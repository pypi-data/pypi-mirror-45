#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

# All next settings must be within the dictionary PROPLAN, when you
# define them in the file settings.py
conf = getattr(settings, 'PROPLAN', {})

# Function allowing access to the application.
ACCESS_FUNCTION = conf.get('ACCESS_FUNCTION', 'proplan.access.view_thread')

# ABS - Automatic Bug System.
# While there is no key, the system does not work.
ABS_KEY = str(conf.get('ABS_KEY', ''))
if ABS_KEY and len(ABS_KEY) < 12:
    raise ImproperlyConfigured(
        'Proplan ABS_KEY is not secure: %s' % ABS_KEY)
# The cookie name for checking the ABS key.
ABS_COOKIE_NAME = conf.get('ABS_COOKIE_NAME', 'proplanabs')

# Path to uploading files.
ATTACH_UPLOAD_PATH = conf.get(
    'ATTACH_UPLOAD_PATH', 'proplan/attaches/%(date)s/%(code)s/%(filename)s')
# The size of the thumbnails for attached images
ATTACH_THUMB_SIZE = conf.get('ATTACH_THUMB_SIZE', (300, 300))
# List of recognized image extensions to be previewed.
ATTACH_THUMB_EXTENSIONS = conf.get('ATTACH_THUMB_EXTENSIONS', [
    '.png', '.jpg', '.jpeg', '.bmp',
])

PRIORITIES = conf.get('PRIORITIES', [
    (1, _('low')),
    (2, _('normal')),
    (3, _('high')),
    (4, _('urgent')),
    (5, _('immediate')),
])
