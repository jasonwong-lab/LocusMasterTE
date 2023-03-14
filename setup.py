# -*- coding: utf-8 -*-
""" Setup LocusMasterTE-ngs package

"""
from __future__ import print_function

from os import path, environ
from distutils.core import setup
from setuptools import Extension
from setuptools import find_packages

from LocusMasterTE._version import VERSION

__author__ = 'Sojung LEE'
__copyright__ = "Copyright (C) 2023 Sojung LEE"

USE_CYTHON = True

CONDA_PREFIX = environ.get("CONDA_PREFIX", '.')
HTSLIB_INCLUDE_DIR = environ.get("HTSLIB_INCLUDE_DIR", None)

htslib_include_dirs = [
    HTSLIB_INCLUDE_DIR,
    path.join(CONDA_PREFIX, 'include'),
    path.join(CONDA_PREFIX, 'include', 'htslib'),
]
htslib_include_dirs = [d for d in htslib_include_dirs if path.exists(str(d)) ]

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    Extension("telescope_scripts.utils.calignment",
              ["telescope_scripts/utils/calignment"+ext],
              include_dirs=htslib_include_dirs,
              ),
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name='LocusMasterTE-ngs',
    version=VERSION.split('+')[0],
    packages=find_packages(),

    install_requires=[
        'future',
        'pyyaml',
        'cython',
        'numpy>=1.16.3',
        'scipy>=1.2.1',
        'pysam>=0.15.2',
        'intervaltree>=3.0.2',
    ],

    # Runnable scripts
    entry_points={
        'console_scripts': [
            'LocusMasterTE=LocusMasterTE.__main__:main',
        ],
    },

    # cython
    ext_modules=extensions,

    # data
    package_data = {
        'LocusMasterTE': [
            'data/alignment.bam',
            'data/annotation.gtf',
            'data/LocusMasterTE_report.tsv'
        ],
    },

    # metadata for upload to PyPI
    author='Sojung LEE',
    author_email='sjlee98@connect.hku.hk',
    description='long-read assisted short-read Transposable Elements quantification(LocusMasterTE)',
    license='MIT',
    keywords='',
    url='https://github.com/jasonwong-lab/LocusMasterTE',

    zip_safe=False
)
