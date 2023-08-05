#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.module_loading import import_string


from proplan.conf import ACCESS_FUNCTION
from proplan.access import check_abs_key

access = import_string(ACCESS_FUNCTION)


def access_required(function=None, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user access.
    """
    def check_perms(user):
        # First, check if the user has permission.
        if access(user):
            return True
        # If you need a 403 handler, throw an exception.
        if raise_exception:
            raise PermissionDenied
        # Or show the entry form.
        return False
    actual_decorator = user_passes_test(check_perms, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def abs_required(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated or not check_abs_key(request):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator
