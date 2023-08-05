# -*- coding: utf-8 -*-

"""
DBL Python API Wrapper
~~~~~~~~~~~~~~~~~~~~~~
A basic wrapper for the discordbots.org API.
:copyright: (c) 2019 Francis Taylor & discordbots.org
:license: MIT, see LICENSE for more details.
"""

__title__ = 'dblpy'
__author__ = 'Francis Taylor'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 Francis Taylor'
__version__ = '0.2'

from collections import namedtuple

from .client import Client
from .errors import *
from .http import HTTPClient

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=2, micro=0, releaselevel='final', serial=0)
