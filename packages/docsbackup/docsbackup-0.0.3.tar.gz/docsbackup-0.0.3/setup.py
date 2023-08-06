#
# THIS FILE IS AUTOMATICALLY CREATED BY release/Snakefile
#
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import sys
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

long_description = open("README.md").read()

setup(
    name="docsbackup",
    version='0.0.3',
    packages=['docsbackup'],
    package_data={
        '': [
            'LICENSE.txt'
        ],
    },

    setup_requires = [
        'setuptools>=17.1',
        'pytest-runner',
    ],
    install_requires = [
        'pandoc',
        'docopt',
        'ruamel-yaml',
    ],

    author="Dennis Terhorst",
    author_email="d.terhorst@fz-juelich.de",
    description="Downloader for Google documents mentioned in an input file",
    long_description=long_description,

    entry_points = {
        'console_scripts': [
            'docsbackup = docsbackup.docsbackup:main',
        ],
    },

    # https://opensource.org/licenses/BSD-2-Clause
    license="BSD",

    url='https://github.com/INM-6/docsbackup',
    # https://pypi.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Backup']
)
