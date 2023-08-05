#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DefaultConfig(AppConfig):
    name = 'proplan'
    verbose_name = _('ProPlan')
