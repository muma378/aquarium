# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
options = {"py2exe":{"compressed": 1,
                     "optimize": 2,
                     "bundle_files": 1,
                     'includes': ['lxml.etree', 'lxml._elementpath', 'gzip']
                     }}
setup(
    version = "1.0.0",
    description = "Spider ... ",
    name = "name for your exe",
    console=["processHandler.py"],
    options=options,
    zipfile=None)
