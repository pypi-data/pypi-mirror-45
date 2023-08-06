import datetime
import json
import uuid

from functools import wraps

import jwt
import six
from werkzeug.local import LocalProxy
from flask import request, jsonify, current_app
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack

from flask_jwt_extended.config import get_access_expires, get_refresh_expires, \
    get_algorithm, get_blacklist_enabled, get_blacklist_checks, get_auth_header
from flask_jwt_extended.exceptions import JWTEncodeError, JWTDecodeError, \
    InvalidHeaderError, NoAuthHeaderError, WrongTokenError, RevokedTokenError, \
    FreshTokenRequired
from flask_jwt_extended.blacklist import check_if_token_revoked, store_token


def get_jwt_identity():
    """
    Returns the identity of the JWT in this context. If no JWT is present,
    None is returned.
    """
    return getattr(ctx_stack.top, 'jwt_identity', None)


def get_jwt_claims():
    """
    Returns the dictionary of custom use claims in this JWT. If no custom user
    claims are present, an empty dict is returned
    """
    return getattr(ctx_stack.top, 'jwt_user_claims', {})


def _encode_access_token(identity, secret, algorithm, token_expire_delta,
                         fresh, user_claims):
    """
    Creates a new access token.

    :param identity: Some identifier of who this client is (most common would be a client id)
    :param secret: Secret key to encode the JWT with
    :param fresh: If this should be a 'fresh' token or not
    :param algorithm: Which algorithm to use for the toek
    :return: Encoded JWT
    """
    # Verify that all of our custom data we are encoding is what we expect
    if not isinstance(user_claims, dict):
        raise JWTEncodeError('user_claims must be a dict')
    if not isinstance(fresh, bool):
        raise JWTEncodeError('fresh must be a bool')
    try:
        json.dumps(user_claims)
    except Exception as e:
        raise JWTEncodeError('Error json serializing user_claims: {}'.format(str(e)))

    # Create the jwt
    now = datetime.datetime.utcnow()
    uid = str(uuid.uuid4())
    token_data = {
        'exp': now + token_expire_delta,
        'iat': now,
        'nbf': now,
        'jti': uid,
        'identity': identity,
        'fresh': fresh,
        'type': 'access',
        'user_claims': user_claims,
    }
    encoded_token = jwt.encode(token_data, secret, algorithm).decode('utf-8')

    # If blacklisting is enabled and configured to store access and refresh tokens,
    # add this token to the store
    blacklist_enabled = get_blacklist_enabled()
    if blacklist_enabled and get_blacklist_checks() == 'all':
        store_token(token_data, revoked=False)
    return encoded_token


def _encode_refresh_token(identity, secret, algorithm, token_expire_delta):
    """
    Creates a new refresh token, which can be used to create subsequent access
    tokens.

    :param identity: Some identifier used to identify the owner of this token
    :param secret: Secret key to encode the JWT with
    :param algorithm: Which algorithm to use for the toek
    :return: Encoded JWT
    """
    now = datetime.datetime.utcnow()
    uid = str(uuid.uuid4())
    token_data = {
        'exp': now + token_expire_delta,
        'iat': now,
        'nbf': now,
        'jti': uid,
        'identity': identity,
        'type': 'refresh',
    }
    encoded_token = jwt.encode(token_data, secret, algorithm).decode('utf-8')

    # If blacklisting is enabled, store this token in our key-value store
    blacklist_enabled = get_blacklist_enabled()
    if blacklist_enabled:
        store_token(token_data, revoked=False)
    return encoded_token


def _decode_jwt(token, secret, algorithm):
    """
    Decodes an encoded JWT

    :param token: The encoded JWT string to decode
    :param secret: Secret key used to encode the JWT
    :param algorithm: Algorithm used to encode the JWT
    :return: Dictionary containing contents of the JWT
    """
    # ext, iat, and nbf are all verified by pyjwt. We just need to make sure
    # that the custom claims we put in the token are present
    data = jwt.decode(token, secret, algorithm=algorithm)
    if 'jti' not in data or not isinstance(data['jti'], six.string_types):
        raise JWTDecodeError("Missing or invalid claim: jti")
    if 'identity' not in data:
        raise JWTDecodeError("Missing claim: identity")
    if 'type' not in data or data['type'] not in ('refresh', 'access'):
        raise JWTDecodeError("Missing or invalid claim: type")
    if data['type'] == 'access':
        if 'fresh' not in data or not isinstance(data['fresh'], bool):
            raise JWTDecodeError("Missing or invalid claim: fresh")
        if 'user_claims' not in data or not isinstance(data['user_claims'], dict):
            raise JWTDecodeError("Missing or invalid claim: user_claims")
    return data


def _decode_jwt_from_request():
    # Verify we have the auth header
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise NoAuthHeaderError("Missing Authorization Header")

    # Make sure the header is valid
    expected_header = get_auth_header()
    parts = auth_header.split()
    if not expected_header:
        if len(parts) != 1:
            msg = "Badly formatted authorization header. Should be '<JWT>'"
            raise InvalidHeaderError(msg)
        token = parts[0]
    else:
        if parts[0] != expected_header or len(parts) != 2:
            msg = "Bad authorization header. Expected '{} <JWT>'".format(expected_header)
            raise InvalidHeaderError(msg)
        token = parts[1]

    secret = _get_secret_key()
    algorithm = get_algorithm()
    return _decode_jwt(token, secret, algorithm)


def _handle_callbacks_on_error(fn):
    """
    Helper decorator that will catch any exceptions we expect to encounter
    when dealing with a JWT, and call the appropriate callback function for
    handling that error. Callback functions can be set in using the *_loader
    methods in jwt_manager.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        m = current_app.jwt_manager

        try:
            return fn(*args, **kwargs)
        except NoAuthHeaderError:
            return m.unauthorized_callback()
        except jwt.ExpiredSignatureError:
            return m.expired_token_callback()
        except (InvalidHeaderError, jwt.InvalidTokenError, JWTDecodeError,
                WrongTokenError) as e:
            return m.invalid_token_callback(str(e))
        except RevokedTokenError:
            return m.revoked_token_callback()
        except FreshTokenRequired:
            return m.needs_fresh_token_callback()
    return wrapper


def jwt_required(fn):
    """
    If you decorate a vew with this, it will ensure that the requester has a valid
    JWT before calling the actual view. This does not check the freshness of the
    token.

    See also: fresh_jwt_required()

    :param fn: The view function to decorate
    """
    @_handle_callbacks_on_error
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Attempt to decode the token
        jwt_data = _decode_jwt_from_request()

        # Verify this is an access token
        if jwt_data['type'] != 'access':
            raise WrongTokenError('Only access tokens can access this endpoint')

        # If blacklisting is enabled, see if this token has been revoked
        blacklist_enabled = get_blacklist_enabled()
        if blacklist_enabled:
            check_if_token_revoked(jwt_data)

        # Save the jwt in the context so that it can be accessed later by
        # the various endpoints that is using this decorator
        ctx_stack.top.jwt_identity = jwt_data['identity']
        ctx_stack.top.jwt_user_claims = jwt_data['user_claims']
        return fn(*args, **kwargs)
    return wrapper


def fresh_jwt_required(fn):
    """
    If you decorate a vew with this, it will ensure that the requester has a valid
    JWT before calling the actual view.

    See also: jwt_required()

    :param fn: The view function to decorate
    """
    @_handle_callbacks_on_error
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Attempt to decode the token
        jwt_data = _decode_jwt_from_request()

        # Verify this is an access token
        if jwt_data['type'] != 'access':
            raise WrongTokenError('Only access tokens can access this endpoint')

        # If blacklisting is enabled, see if this token has been revoked
        blacklist_enabled = get_blacklist_enabled()
        if blacklist_enabled:
            check_if_token_revoked(jwt_data)

        # Check if the token is fresh
        if not jwt_data['fresh']:
            raise FreshTokenRequired('Fresh token required')

        # Save the jwt in the context so that it can be accessed later by
        # the various endpoints that is using this decorator
        ctx_stack.top.jwt_identity = jwt_data['identity']
        ctx_stack.top.jwt_user_claims = jwt_data['user_claims']
        return fn(*args, **kwargs)
    return wrapper


def jwt_refresh_token_required(fn):
    """
    If you decorate a view with this, it will insure that the requester has a
    valid JWT refresh token before calling the actual view. If the token is
    invalid, expired, not present, etc, the appropiate callback will be called
    """
    @_handle_callbacks_on_error
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the JWT
        jwt_data = _decode_jwt_from_request()

        # verify this is a refresh token
        if jwt_data['type'] != 'refresh':
            raise WrongTokenError('Only refresh tokens can access this endpoint')

        # If blacklisting is enabled, see if this token has been revoked
        blacklist_enabled = get_blacklist_enabled()
        if blacklist_enabled:
            check_if_token_revoked(jwt_data)

        # Save the jwt in the context so that it can be accessed later by
        # the various endpoints that is using this decorator
        ctx_stack.top.jwt_identity = jwt_data['identity']
        return fn(*args, **kwargs)
    return wrapper


def create_refresh_token(identity):
    # Token settings
    refresh_expire_delta = get_refresh_expires()
    algorithm = get_algorithm()
    secret = _get_secret_key()

    # Actually make the tokens
    refresh_token = _encode_refresh_token(identity, secret, algorithm,
                                          refresh_expire_delta)
    return refresh_token


def create_access_token(identity, fresh=True):
    # Token options
    secret = _get_secret_key()
    access_expire_delta = get_access_expires()
    algorithm = get_algorithm()
    user_claims = current_app.jwt_manager.user_claims_callback(identity)
    access_token = _encode_access_token(identity, secret, algorithm, access_expire_delta,
                                        fresh=fresh, user_claims=user_claims)
    return access_token


def _get_secret_key():
    key = current_app.config.get('SECRET_KEY', None)
    if not key:
        raise RuntimeError('flask SECRET_KEY must be set')
    return key
