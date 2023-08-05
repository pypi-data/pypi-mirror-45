# -*- coding: utf-8 -*-
import json

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from proplan import models
from proplan.logic import create_attachment, similarity_checking


class AttachmentForm(forms.Form):
    file = forms.FileField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AttachmentForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data['file']
        if not hasattr(file, 'content_type'):
            raise forms.ValidationError(_('Parameter "file" is not valid.'))
        name = file.name
        if '.' not in name:
            raise forms.ValidationError(_('File not contain extension.'))
        if '/' in name:
            raise forms.ValidationError(_('File name is contains slash.'))
        return file

    def save(self):
        file = self.cleaned_data['file']
        return create_attachment(self.user, file)


class TrackerForm(forms.ModelForm):

    class Meta:
        model = models.Tracker
        exclude = []


class StageForm(forms.ModelForm):

    class Meta:
        model = models.Stage
        exclude = []


class RoleForm(forms.ModelForm):

    class Meta:
        model = models.Role
        exclude = []


class CheckThreadMixing:

    def similarity_checking(self, cleaned_data):
        thread = self.instance
        other = similarity_checking(
            cleaned_data.get('title', thread.title),
            cleaned_data.get('message', thread.message),
            thread.is_abs,
            exclude_id=thread.id,
        )
        if other:
            raise forms.ValidationError(
                _('Similarity theads is exists: %(other)s.'),
                params={'other': other}
            )


class ThreadCreateForm(CheckThreadMixing, forms.ModelForm):

    class Meta:
        model = models.Thread
        fields = [
            'parent', 'tracker', 'stage', 'priority', 'title',
            'message', 'attachments',
        ]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        if 'instance' not in kwargs:
            kwargs['instance'] = models.Thread(author=user, is_abs=False)
        super(ThreadCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        self.similarity_checking(cleaned_data)
        return cleaned_data


class ThreadChangeForm(CheckThreadMixing, forms.ModelForm):

    comment = forms.CharField(required=False)

    class Meta:
        model = models.Thread
        fields = [
            'parent', 'tracker', 'stage', 'priority', 'title',
            'message', 'attachments',
        ]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        assert 'instance' in kwargs
        super(ThreadChangeForm, self).__init__(*args, **kwargs)

    def make_diff(self, data):
        self.diff = diff = {}
        instance = self.instance
        for name in self.changed_data:
            if name == 'comment':
                continue
            if name == 'attachments':
                old = list(instance.attachments.values_list('id', flat=True))
                new = data.get(name)
                if new is None:
                    new = []
                else:
                    new = list(new.values_list('id', flat=True))
                old.sort()
                new.sort()
            else:
                old = force_text(getattr(instance, name))
                new = force_text(data.get(name))
            diff[name] = [old, new]
        return diff

    def clean(self):
        cleaned_data = super().clean()
        self.similarity_checking(cleaned_data)
        self.make_diff(cleaned_data)
        return cleaned_data

    def save(self, *args, **kwargs):
        thread = super().save(*args, **kwargs)
        message = self.cleaned_data['comment']
        changes = json.dumps(self.diff)
        comment = models.Comment(
            user=self.user, thread=thread,
            message=message, changes=changes)
        comment.save()
        return thread


class ABSThreadCreateForm(CheckThreadMixing, forms.ModelForm):
    """
    Form for creating thread from Automaic Bug System.

    """

    class Meta:
        model = models.Thread
        fields = ['parent', 'title', 'message', 'attachments']

    def __init__(self, *args, **kwargs):
        if 'instance' not in kwargs:
            kwargs['instance'] = models.Thread(
                is_abs=True,
                tracker=models.Tracker.objects.get_abs(),
                stage=models.Stage.objects.get_abs(),
            )
        super(ABSThreadCreateForm, self).__init__(*args, **kwargs)

    def clean_tracker(self):
        tracker = self.cleaned_data['tracker']
        if not tracker.is_abs:
            raise forms.ValidationError(_('Tracker is not for ABS.'))
        return tracker

    def clean_stage(self):
        stage = self.cleaned_data['stage']
        if not stage.is_abs:
            raise forms.ValidationError(_('Stage is not for ABS.'))
        return stage

    def clean(self):
        instance = self.instance
        if not (instance.tracker and instance.stage):
            raise forms.ValidationError(
                _('The ABS is not ready to accept errors.'))
        return super().clean()


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['thread', 'message', 'attachments']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        if 'instance' not in kwargs:
            kwargs['instance'] = models.Comment(user=user)
        super(CommentCreateForm, self).__init__(*args, **kwargs)


class CommentChangeForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['message', 'attachments']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        assert 'instance' in kwargs
        super(CommentChangeForm, self).__init__(*args, **kwargs)


class ExecutorCreateForm(forms.ModelForm):

    class Meta:
        model = models.Executor
        fields = ['thread', 'user', 'role']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ExecutorCreateForm, self).__init__(*args, **kwargs)


class ExecutorChangeForm(forms.ModelForm):

    class Meta:
        model = models.Executor
        fields = ['role']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        assert 'instance' in kwargs
        super(ExecutorChangeForm, self).__init__(*args, **kwargs)
