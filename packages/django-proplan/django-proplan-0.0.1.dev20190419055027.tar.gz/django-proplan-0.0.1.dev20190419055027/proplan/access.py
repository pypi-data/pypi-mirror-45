#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
"""
Functions for access control.
"""
from proplan.conf import ABS_COOKIE_NAME, ABS_KEY


def authenticated(user):
    """For authenticated users."""
    return user.is_active and user.is_authenticated


def staff(user):
    """For employers and superusers."""
    return authenticated(user) and (user.is_staff or user.is_superuser)


def superuser(user):
    """For superusers only."""
    return authenticated(user) and user.is_superuser


def view_thread(user):
    """For users with view permission for Thread model."""
    return authenticated(user) and user.has_perm('proplan.view_thread')


def check_abs_key(request):
    """Checks the request for Automatic Bug System."""
    key = request.COOKIES.get(ABS_COOKIE_NAME, '')
    if key == ABS_KEY:
        request.META['ABS_KEY'] = key
        return True
    if 'ABS_KEY' in request.META:
        request.META.pop('ABS_KEY')
    return False
