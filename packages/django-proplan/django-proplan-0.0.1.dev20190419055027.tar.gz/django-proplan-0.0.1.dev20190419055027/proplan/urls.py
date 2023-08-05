#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.urls import path, include
from proplan.views import pages, api, auto

app_name = 'proplan'

abs_patterns = [
    path('upload/', auto.UploadView.as_view(), name='upload'),
    path('create/', auto.CreateView.as_view(), name='create'),
    path('', auto.check, name='check'),
]

api_patterns = [
    path('attachments/', api.AttachmentsView.as_view(), name='attachments'),
    path('attachments/<int:id>/', api.AttachmentView.as_view(), name='attachment'),
    path('trackers/', api.TrackersView.as_view(), name='trackers'),
    path('trackers/<int:id>/', api.TrackerView.as_view(), name='tracker'),
    path('stages/', api.StagesView.as_view(), name='stages'),
    path('stages/<int:id>/', api.StageView.as_view(), name='stage'),
    path('roles/', api.RolesView.as_view(), name='roles'),
    path('roles/<int:id>/', api.RoleView.as_view(), name='role'),
    path('threads/', api.ThreadsView.as_view(), name='threads'),
    path('threads/<int:id>/', api.ThreadView.as_view(), name='thread'),
    path('comments/', api.CommentsView.as_view(), name='comments'),
    path('comments/<int:id>/', api.CommentView.as_view(), name='comment'),
    path('executors/', api.ExecutorsView.as_view(), name='executors'),
    path('executors/<int:id>/', api.ExecutorView.as_view(), name='executor'),
    path('start/<int:id>/', api.StartView.as_view(), name='start'),
    path('stop/<int:id>/', api.StopView.as_view(), name='stop'),
]


pages_patterns = [
    # path('settings/', pages.SettingsView.as_view(), name='settings'),
    path('attachments/', pages.AttachmentsView.as_view(), name='attachments'),
    path('threads/', pages.ThreadsView.as_view(), name='threads'),
    path('', pages.IndexView.as_view(), name='index'),
]

urlpatterns = [
    path('api/', include((api_patterns, 'api'))),
    path('abs/', include((abs_patterns, 'abs'))),
    path('', include(pages_patterns)),
]
