#!/usr/bin/env python
from __future__ import print_function

import os
import os.path
import sys
from setuptools import setup
import textwrap


name = 'iris_grib'


LONG_DESCRIPTION = textwrap.dedent("""
    Iris loading of GRIB files
    ==========================

    With this package, iris is able to load GRIB files:

    ```
    my_data = iris.load(path_to_grib_file)
    ```
    """)


here = os.path.abspath(os.path.dirname(__file__))
pkg_root = os.path.join(here, name)

packages = []
for d, _, _ in os.walk(os.path.join(here, name)):
    if os.path.exists(os.path.join(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))


def extract_version():
    version = None
    fdir = os.path.dirname(__file__)
    fnme = os.path.join(fdir, 'iris_grib', '__init__.py')
    with open(fnme) as fd:
        for line in fd:
            if (line.startswith('__version__')):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters
                break
    return version


def file_walk_relative(top, remove=''):
    """
    Returns a generator of files from the top of the tree, removing
    the given prefix from the root/file result.

    """
    top = top.replace('/', os.path.sep)
    remove = remove.replace('/', os.path.sep)
    for root, dirs, files in os.walk(top):
        for file in files:
            yield os.path.join(root, file).replace(remove, '')


setup_args = dict(
    name             = name,
    version          = extract_version(),
    packages         = packages,
    package_data     = {'iris_grib': list(file_walk_relative('iris_grib/tests/results',
                                          remove='iris_grib/'))},
    description      = "GRIB loading for Iris",
    long_description = LONG_DESCRIPTION,
    url              = 'https://github.com/SciTools/iris-grib',
    author           = 'UK Met Office',
    author_email     = 'scitools-iris@googlegroups.com',
    license          = 'LGPL',
    platforms        = "Linux, Mac OS X, Windows",
    keywords         = ['iris', 'GRIB'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    # XXX: This is a royal dependency mess at the moment. The PyPI eccodes
    # package 2.10.0 is a wheel for win_amd64 only, so we'll only add that as
    # a dependence for the relevant platform, otherwise unfortunately it's up
    # to the user to provision themselves until ECMWF and PyPI provide the
    # suitable package platform coverage.
    install_requires=['scitools-iris>=2.0.*'] + [
        'eccodes-python'] if 'win' in sys.platform else [],
    extras_require={
        'test:python_version=="2.7"': ['mock']
    },
    test_suite = 'iris_grib.tests',
)


if __name__ == '__main__':
    setup(**setup_args)
