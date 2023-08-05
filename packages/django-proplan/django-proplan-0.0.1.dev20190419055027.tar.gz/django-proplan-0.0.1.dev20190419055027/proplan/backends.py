#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.contrib.auth.models import Permission
from django.contrib.auth.backends import ModelBackend


class ExtraModelBackend(ModelBackend):

    def _get_role_permissions(self, user_obj):
        return Permission.objects.filter(proplan_roles__users=user_obj)

    def get_role_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        roles they belong.
        """
        return self._get_permissions(user_obj, obj, 'role')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = {
                *self.get_user_permissions(user_obj),
                *self.get_group_permissions(user_obj),
                *self.get_role_permissions(user_obj),
            }
        return user_obj._perm_cache
