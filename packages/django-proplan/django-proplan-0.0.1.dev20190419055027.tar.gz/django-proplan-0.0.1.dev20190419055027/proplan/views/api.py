#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
"""
JSON REST API views for users.
"""
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
# from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.views.generic import View

from proplan import forms
from proplan.models import (
    Attachment, Tracker, Stage, Role, Thread, Comment, Executor,
)
from proplan.logic import Controller
from proplan.serializers import ExecutorSerializer, ThreadSerializer
from proplan.views.base import parse_params, AccessMixin, BaseUploadView


attachment_ctrl = Controller(Attachment)


class AttachmentsView(AccessMixin, BaseUploadView):
    """Uploads and views attachments."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_attachment'):
            raise PermissionDenied
        page, orders, filters = attachment_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_attachment'):
            raise PermissionDenied
        return self.upload_attachment(request)


class AttachmentView(AccessMixin, View):
    """Managing one attachment."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_attachment'):
            raise PermissionDenied
        obj = get_object_or_404(Attachment, id=id)
        data = attachment_ctrl.serializer(obj)
        return JsonResponse(data)

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_attachment'):
            raise PermissionDenied
        obj = get_object_or_404(Attachment, id=id)
        obj.delete()
        return JsonResponse({'id': id})


tracker_ctrl = Controller(Tracker)


class TrackersView(AccessMixin, View):
    """Getting and posting trackers."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_tracker'):
            raise PermissionDenied
        page, orders, filters = tracker_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_tracker'):
            raise PermissionDenied
        form = forms.TrackerForm(parse_params(request))
        if form.is_valid():
            tracker = form.save()
            data = tracker_ctrl.serializer(tracker)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class TrackerView(AccessMixin, View):
    """Managing one tracker."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_tracker'):
            raise PermissionDenied
        obj = get_object_or_404(Tracker, id=id)
        data = tracker_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        if not user.has_perm('proplan.change_tracker'):
            raise PermissionDenied
        obj = get_object_or_404(Tracker, id=id)
        form = forms.TrackerForm(parse_params(request), instance=obj)
        if form.is_valid():
            tracker = form.save()
            data = tracker_ctrl.serializer(tracker)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_tracker'):
            raise PermissionDenied
        obj = get_object_or_404(Tracker, id=id)
        obj.delete()
        return JsonResponse({'id': id})


stage_ctrl = Controller(Stage)


class StagesView(AccessMixin, View):
    """Getting and posting stages."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_stage'):
            raise PermissionDenied
        page, orders, filters = stage_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_stage'):
            raise PermissionDenied
        form = forms.StageForm(parse_params(request))
        if form.is_valid():
            stage = form.save()
            data = stage_ctrl.serializer(stage)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class StageView(AccessMixin, View):
    """Managing one stage."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_stage'):
            raise PermissionDenied
        obj = get_object_or_404(Stage, id=id)
        data = stage_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        if not user.has_perm('proplan.change_stage'):
            raise PermissionDenied
        obj = get_object_or_404(Stage, id=id)
        form = forms.StageForm(parse_params(request), instance=obj)
        if form.is_valid():
            stage = form.save()
            data = stage_ctrl.serializer(stage)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_stage'):
            raise PermissionDenied
        obj = get_object_or_404(Stage, id=id)
        obj.delete()
        return JsonResponse({'id': id})


role_ctrl = Controller(Role)


class RolesView(AccessMixin, View):
    """Getting and posting user roles."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_role'):
            raise PermissionDenied
        page, orders, filters = role_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_role'):
            raise PermissionDenied
        form = forms.RoleForm(parse_params(request))
        if form.is_valid():
            role = form.save()
            data = role_ctrl.serializer(role)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class RoleView(AccessMixin, View):
    """Managing one user role."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_role'):
            raise PermissionDenied
        obj = get_object_or_404(Role, id=id)
        data = role_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        if not user.has_perm('proplan.change_role'):
            raise PermissionDenied
        obj = get_object_or_404(Role, id=id)
        form = forms.RoleForm(parse_params(request), instance=obj)
        if form.is_valid():
            role = form.save()
            data = role_ctrl.serializer(role)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_role'):
            raise PermissionDenied
        obj = get_object_or_404(Role, id=id)
        obj.delete()
        return JsonResponse({'id': id})


thread_ctrl = Controller(Thread, serializer=ThreadSerializer)


class ThreadsView(AccessMixin, View):
    """Getting and posting threads."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_thread'):
            raise PermissionDenied
        page, orders, filters = thread_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_thread'):
            raise PermissionDenied
        form = forms.ThreadCreateForm(user, parse_params(request))
        if form.is_valid():
            thread = form.save()
            data = thread_ctrl.serializer(thread)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class ThreadView(AccessMixin, View):
    """Managing one thread."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_thread'):
            raise PermissionDenied
        obj = get_object_or_404(Thread, id=id)
        data = thread_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        if not user.has_perm('proplan.change_thread'):
            raise PermissionDenied
        obj = get_object_or_404(Thread, id=id)
        form = forms.ThreadChangeForm(
            user, parse_params(request), instance=obj)
        if form.is_valid():
            thread = form.save()
            # print(form.diff)
            data = thread_ctrl.serializer(thread)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_thread'):
            raise PermissionDenied
        obj = get_object_or_404(Thread, id=id)
        obj.delete()
        return JsonResponse({'id': id})


comment_ctrl = Controller(Comment)


class CommentsView(AccessMixin, View):
    """Getting and posting comments."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_comment'):
            raise PermissionDenied
        page, orders, filters = comment_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_comment'):
            raise PermissionDenied
        form = forms.CommentCreateForm(user, parse_params(request))
        if form.is_valid():
            comment = form.save()
            data = comment_ctrl.serializer(comment)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class CommentView(AccessMixin, View):
    """Managing one comment."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_comment'):
            raise PermissionDenied
        obj = get_object_or_404(Comment, id=id)
        data = comment_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        obj = get_object_or_404(Comment, id=id)
        if obj.user == user:
            pass
        elif not user.has_perm('proplan.change_comment'):
            raise PermissionDenied
        form = forms.CommentChangeForm(
            user, parse_params(request), instance=obj)
        if form.is_valid():
            comment = form.save()
            data = comment_ctrl.serializer(comment)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_comment'):
            raise PermissionDenied
        obj = get_object_or_404(Comment, id=id)
        obj.delete()
        return JsonResponse({'id': id})


executor_ctrl = Controller(Executor, serializer=ExecutorSerializer)


class ExecutorsView(AccessMixin, View):
    """Getting and posting executors."""

    def get(self, request):
        user = request.user
        if not user.has_perm('proplan.view_executor'):
            raise PermissionDenied
        page, orders, filters = executor_ctrl.get_serialized(request)
        data = {'page': page, 'orders': orders, 'filters': filters}
        return JsonResponse(data)

    def post(self, request):
        user = request.user
        if not user.has_perm('proplan.add_executor'):
            raise PermissionDenied
        form = forms.ExecutorCreateForm(user, parse_params(request))
        if form.is_valid():
            executor = form.save()
            data = executor_ctrl.serializer(executor)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)


class ExecutorView(AccessMixin, View):
    """Managing one executor."""

    def get(self, request, id):
        user = request.user
        if not user.has_perm('proplan.view_executor'):
            raise PermissionDenied
        obj = get_object_or_404(Executor, id=id)
        data = executor_ctrl.serializer(obj)
        return JsonResponse(data)

    def patch(self, request, id):
        user = request.user
        obj = get_object_or_404(Executor, id=id)
        if obj.user == user:
            pass
        elif not user.has_perm('proplan.change_executor'):
            raise PermissionDenied
        form = forms.ExecutorChangeForm(
            user, parse_params(request), instance=obj)
        if form.is_valid():
            executor = form.save()
            data = executor_ctrl.serializer(executor)
            return JsonResponse(data)
        data = {'errors': form.errors.get_json_data(escape_html=True)}
        return JsonResponse(data, status=400)

    put = patch

    def delete(self, request, id):
        user = request.user
        if not user.has_perm('proplan.delete_executor'):
            raise PermissionDenied
        obj = get_object_or_404(Executor, id=id)
        obj.delete()
        return JsonResponse({'id': id})


class StartView(AccessMixin, View):
    """Starting executor work."""

    def post(self, request, id):
        user = request.user
        qs = Executor.objects.select_related('thread__stage')
        executor = get_object_or_404(qs, id=id)
        if executor.thread.stage.is_finished:
            raise PermissionDenied
        elif executor.user == user:
            pass
        elif not user.has_perm('proplan.start_other_executor'):
            raise PermissionDenied
        if not executor.sprint:
            executor.start_sprint(save=True)
        return JsonResponse({
            'id': executor.id,
            'start': executor.sprint,
            'time_total': executor.time_total,
            'time_work': executor.time_work,
        })


class StopView(AccessMixin, View):
    """Stop executor work."""

    def post(self, request, id):
        user = request.user
        qs = Executor.objects.select_related('thread__stage')
        executor = get_object_or_404(qs, id=id)
        if executor.user == user:
            pass
        elif not user.has_perm('proplan.stop_other_executor'):
            raise PermissionDenied
        if executor.sprint:
            executor.stop_sprint(save=True)
        return JsonResponse({
            'id': executor.id,
            'stop': executor.stop,
            'time_total': executor.time_total,
            'time_work': executor.time_work,
        })
