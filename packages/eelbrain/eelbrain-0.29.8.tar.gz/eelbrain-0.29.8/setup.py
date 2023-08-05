"""
setup.py
========

This is the setup.py script for Eelbrain.

http://docs.python.org/distutils/index.html
https://setuptools.readthedocs.io/en/latest/setuptools.html


About MANIFEST.in:

https://docs.python.org/2/distutils/sourcedist.html#manifest-template

"""
# Setuptools bootstrap module
# http://pythonhosted.org//setuptools/setuptools.html
from ez_setup import use_setuptools
use_setuptools('17')

from distutils.version import LooseVersion
from distutils.extension import Extension
from glob import glob
from os.path import pathsep
import re
from setuptools import setup, find_packages

import numpy as np

# Distributing Cython modules
# https://cython.readthedocs.io/en/stable/src/userguide/source_files_and_compilation.html#distributing-cython-modules
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = False


DESC = """
GitHub: https://github.com/christianbrodbeck/Eelbrain
"""

# version must be in X.X.X format, e.g., "0.0.3dev"
with open('eelbrain/__init__.py') as fid:
    text = fid.read()
match = re.search(r"__version__ = '([.\w]+)'", text)
if match is None:
    raise ValueError("No valid version string found in:\n\n" + text)
version = match.group(1)
LooseVersion(version)  # check that it's a valid version

# Cython extensions
ext_paths = ('eelbrain/*%s', 'eelbrain/_trf/*%s', 'eelbrain/_stats/*%s')
if cythonize is False:
    actual_paths = []
    for path in ext_paths:
        actual_paths.extend(glob(path % '.c'))
    ext_modules = [
        Extension(path.replace(pathsep, '.')[:-2], [path])
        for path in actual_paths
    ]
else:
    ext_modules = cythonize([path % '.pyx' for path in ext_paths])

setup(
    name='eelbrain',
    version=version,
    description="MEG/EEG analysis tools",
    url="http://eelbrain.readthedocs.io",
    author="Christian Brodbeck",
    author_email='christianbrodbeck@nyu.edu',
    license='BSD (3-clause)',
    long_description=DESC,
    python_requires='>=3.6',
    setup_requires=[
        "numpy >= 1.11",
        "cython >= 0.21",
    ],
    extras_require={
        'base': [
            'colormath >= 2.1',
            'keyring >= 5',
            'mne >= 0.17',
            'nibabel >= 2.0',
            'pillow',
            'tqdm >= 4.8',
        ],
        'full': [
            'numpy >= 1.8',
            'scipy >= 0.17',
            'matplotlib >= 2.1',
        ],
        'plot.brain': [
            'pysurfer[save_movie] >= 0.8',
        ],
    },
    include_dirs=[np.get_include()],
    packages=find_packages(),
    ext_modules=ext_modules,
    scripts=['bin/eelbrain'],
)
