# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Framework :: Sphinx :: Extension",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Documentation",
    "Topic :: Documentation :: Sphinx",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Testing",
    "Topic :: Text Processing :: Markup",
    "Topic :: Utilities",
]
description = 'testing utility classes and functions for Sphinx extensions'

test_require = []
if sys.version_info < (2, 7):
    test_require.append('unittest2')

if sys.version_info < (3, 3):
    test_require.append('mock')

setup(
    name='sphinx-testing',
    version='1.0.1',
    description=description,
    long_description=description,
    classifiers=classifiers,
    keywords=['sphinx', 'testing'],
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    url='https://github.com/sphinx-doc/sphinx-testing',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Sphinx',
        'six',
    ],
    tests_require=test_require,
)
