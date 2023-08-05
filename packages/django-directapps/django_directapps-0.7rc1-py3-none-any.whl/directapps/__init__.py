#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import os
from directapps import version

default_app_config = 'directapps.apps.AppConfig'

VERSION = (0, 7, 0, 'rc', 1)


def get_version():
    path = os.path.dirname(os.path.abspath(__file__))
    return version.get_version(VERSION, path)


__version__ = get_version()
