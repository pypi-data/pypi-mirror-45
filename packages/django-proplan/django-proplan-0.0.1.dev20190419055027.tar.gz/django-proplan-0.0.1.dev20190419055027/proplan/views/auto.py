#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
"""
JSON REST API views for Automatic Bug System.
"""
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import View

from proplan import forms
from proplan.conf import ABS_KEY
from proplan.models import Tracker, Stage
from proplan.views.base import parse_params, ABSMixin, BaseUploadView


@cache_page(60 * 5)
def check(request):
    """Checking the ready ABS."""
    ready = bool(
        ABS_KEY and
        Tracker.objects.get_abs() and
        Stage.objects.get_abs()
    )
    if ready:
        message = _('The ABS is ready to accept errors.')
    else:
        message = _('The ABS is not ready to accept errors.')
    data = {
        'ready': ready,
        'message': message,
    }
    return JsonResponse(data)


class UploadView(ABSMixin, BaseUploadView):
    """Uploads attachments from Automatic Bug System."""
    pass


class CreateView(ABSMixin, View):
    """Posting threads from Automatic Bug System."""

    def post(self, request):
        form = forms.ABSThreadCreateForm(parse_params(request))
        if form.is_valid():
            thread = form.save()
            data = {
                'id': thread.id,
                'title': thread.title,
            }
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)
