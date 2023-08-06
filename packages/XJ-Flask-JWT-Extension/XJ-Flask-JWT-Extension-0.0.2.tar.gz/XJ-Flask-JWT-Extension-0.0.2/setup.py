"""
Flask-JWT-Extension
-------------------
Flask-Login provides jwt endpoint protection for Flask.
"""
from setuptools import setup

setup(name='XJ-Flask-JWT-Extension',
      version='0.0.2',
      url='https://github.com/caser789/flask-jwt',
      license='MIT',
      author='Xue Jiao',
      author_email='jiao.xuejiao@gmail.com',
      description='Extended JWT integration with Flask',
      long_description='Extended JWT integration with Flask',
      keywords = ['flask', 'jwt', 'json web token'],
      packages=['flask_jwt_extended'],
      zip_safe=False,
      platforms='any',
      install_requires=['Flask', 'PyJWT', 'simplekv', 'six'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ])
