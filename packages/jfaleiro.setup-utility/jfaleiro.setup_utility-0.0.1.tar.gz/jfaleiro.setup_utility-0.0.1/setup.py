#!/usr/bin/env python
#
#     setup_utility - Shared helpers for setuptools configuration.
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pathlib

from setuptools import setup, find_packages

from setup_utility import (
    BehaveTestCommand,
    CleanCommand,
    LicenseHeaderCommand,
    ToxCommand,
    version_from_git
)


setup(
    name='jfaleiro.setup_utility',
    version=version_from_git(),
    description='Shared helpers for setuptools configuration',
    long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Jorge M. Faleiro Jr.',
    author_email='j@falei.ro',
    url='https://gitlab.com/jfaleiro/setup_utility',
    download_url='https://github.com/jfaleiro/setup_utility/tarball/master',
    license="Affero GPL, see LICENSE for details",
    packages=find_packages(),
    py_modules=[
        'setup_utility',
    ],
    cmdclass={
        'behave_test': BehaveTestCommand,
        'clean': CleanCommand,
        'license_headers': LicenseHeaderCommand,
        'tox': ToxCommand,
    },
    setup_requires=[
        'setupext-janitor',
        'behave',
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'PyHamcrest',
    ],
    test_suite='nose.collector',
    install_requires=[
        'behave',
        'nose>=1.0',
        'coverage',
        'mock',
        'pytest-runner',
        'pytest',
        'PyHamcrest',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
