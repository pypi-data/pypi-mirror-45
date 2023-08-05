#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
# from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from proplan import forms
from proplan.models import Attachment, Thread
from proplan.logic import Controller
from proplan.views.base import AccessMixin


class IndexView(AccessMixin, TemplateView):
    template_name = 'proplan/index.html'


class AttachmentsView(AccessMixin, TemplateView):
    """List of uploaded attachments from user."""
    template_name = 'proplan/attachments.html'
    ctrl = Controller(Attachment)

    @property
    def extra_context(self):
        user = self.request.user
        form = forms.AttachmentForm(user)
        page, orders, filters = self.ctrl.get(self.request)
        ctx = {
            'page': page,
            'orders': orders,
            'filters': filters,
            'form': form,
        }
        return ctx


class ThreadsView(AccessMixin, TemplateView):
    """List threads for users."""
    template_name = 'proplan/threads.html'
    ctrl = Controller(Thread)

    @property
    def extra_context(self):
        page, orders, filters = self.ctrl.get(self.request)
        ctx = {
            'page': page,
            'orders': orders,
            'filters': filters,
        }
        return ctx
