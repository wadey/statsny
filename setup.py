# -*- coding: utf-8 -*-
#
# © 2010 SimpleGeo, Inc. All rights reserved.
#

import os
from setuptools import setup, find_packages

PKG="statsny"
__VERSION_FILE = os.path.join(PKG, '_version.py')
__VERSION_LOCALS={}

execfile(__VERSION_FILE, __VERSION_LOCALS)

if '__version__' not in __VERSION_LOCALS:
    raise RuntimeError("No __version__ defined in in %s." % __VERSION_FILE)

version = str(__VERSION_LOCALS['__version__'])

setup(name=PKG,
      version=version,
      packages=find_packages(),
      install_requires=["twisted",
                        "ostrich>=0.3.9",
                        "simplejson"])
