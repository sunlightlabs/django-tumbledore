#!/usr/bin/env python
# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

from tumbledore import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    name       = __appname__,
    version    = __version__,
    packages   = ['tumbledore', 'tumbledore.templatetags', 'tumbledore.migrations'],

    author       = "Dan Drinkard",
    author_email = "ddrinkard@sunlightfoundation.com",

    long_description = long_description,
    description      = 'A simple, barebones tumblelog implementation for your django site',
    license          = "BSD",
    url              = "https://github.com/sunlightlabs/django-tumbledore",

    platforms        = ['any'],
    install_requires = ['jsonfield', ]
)
