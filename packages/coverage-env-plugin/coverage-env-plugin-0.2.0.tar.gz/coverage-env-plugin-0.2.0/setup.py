#!/usr/bin/env python

from setuptools import setup

classifiers = """\
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
Development Status :: 4 - Beta
"""

setup(
    name='coverage-env-plugin',
    version='0.2.0',
    description='coverage.py environment plugin',
    author='John Vandenberg',
    author_email='jayvdb@gmail.com',
    url='https://github.com/jayvdb/coverage_env_plugin',
    py_modules=['coverage_env_plugin'],
    install_requires=[
        'coverage >= 4.0',
        'packaging',
    ],
    tests_require=['unittest-mixins'],
    test_suite='tests',
    license='MIT License',
    classifiers=classifiers.splitlines(),
)
