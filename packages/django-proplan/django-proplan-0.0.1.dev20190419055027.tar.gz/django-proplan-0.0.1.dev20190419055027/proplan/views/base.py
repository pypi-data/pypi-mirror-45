#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from json import loads

from django.http import QueryDict, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from proplan import forms
from proplan.decorators import access_required, abs_required


def parse_params(request):
    if request.content_type == 'application/json':
        return loads(request.body.decode('utf-8'))
    method = request.method
    if method == 'GET':
        return request.GET
    elif method == 'POST':
        return request.POST
    return QueryDict(request.body)


@method_decorator(access_required, name='dispatch')
class AccessMixin:
    """Mixing for user access."""
    def dispatch(self, *args, **kwargs):
        return super(AccessMixin, self).dispatch(*args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(abs_required, name='dispatch')
class ABSMixin:
    """Mixing for Automatic Bug System access."""
    def dispatch(self, *args, **kwargs):
        return super(ABSMixin, self).dispatch(*args, **kwargs)


class BaseUploadView(View):
    """View for uploading attachments."""

    def upload_attachment(self, request):
        form = forms.AttachmentForm(request.user, files=request.FILES)
        if form.is_valid():
            attachment = form.save()
            data = {
                'id': attachment.id,
                'name': attachment.name,
                'url': attachment.url,
                'thumb': attachment.thumb_url,
            }
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    def post(self, request):
        return self.upload_attachment(request)
