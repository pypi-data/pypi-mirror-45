#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Setup module """

import os
import re
from io import open

from setuptools import setup

# Get version from __init__.py file
VERSION = ""
with open("wordpress/__init__.py", "r") as fd:
    VERSION = re.search(
        r"^__version__\s*=\s*['\"]([^\"]*)['\"]", fd.read(), re.MULTILINE
    ).group(1)

if not VERSION:
    raise RuntimeError("Cannot find version information")

# Get long description
README = open(os.path.join(os.path.dirname(__file__),
                           "README.rst"), encoding="utf8").read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wordpress-api",
    version=VERSION,
    description=(
        "A Python wrapper for the Wordpress and WooCommerce REST APIs "
        "with oAuth1a 3leg support"
    ),
    long_description=README,
    author="Claudio Sanches @ Automattic, forked by Derwent @ Laserphile",
    url="https://github.com/derwentx/wp-api-python",
    license="MIT License",
    packages=[
        "wordpress"
    ],
    include_package_data=True,
    platforms=['any'],
    install_requires=[
        "requests",
        "requests_oauthlib",
        "ordereddict",
        "beautifulsoup4",
        'lxml',
        'six',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'httmock',
        'pytest',
        'six'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords='python wordpress woocommerce api development'
)
