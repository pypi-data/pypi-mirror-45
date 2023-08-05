#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import os
from proplan import version

default_app_config = 'proplan.apps.DefaultConfig'

VERSION = (0, 0, 1, 'alpha', 0)


def get_version():
    path = os.path.dirname(os.path.abspath(__file__))
    return version.get_version(VERSION, path)


__version__ = get_version()
