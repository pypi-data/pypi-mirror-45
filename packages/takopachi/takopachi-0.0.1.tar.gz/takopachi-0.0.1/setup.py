#!/usr/bin/env python -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='takopachi',
    version='0.0.1',
    packages=['takopachi'],
    description='Takopachi',
    long_description='',
    url = 'https://git.hikari.prod.rsc.local/liling.tan/takopachi',
    #package_data={'takopachi': [,]},
    license="MIT",
    install_requires = ['beautifulsoup4', 'lazyme', 'tqdm', 'requests']
)
