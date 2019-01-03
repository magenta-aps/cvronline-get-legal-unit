#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from setuptools import setup

setup(
    name='cvronline_get_legal_unit',
    py_modules=['cvronline_get_legal_unit'],
    version=open('VERSION').read(),
    long_description=open('README.md').read(),
    install_requires=[
        "xmltodict",
        "requests"
    ]
)
