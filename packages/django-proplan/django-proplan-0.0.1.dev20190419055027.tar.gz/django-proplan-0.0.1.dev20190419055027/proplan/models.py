#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from os import (
    path as os_path, remove as os_remove, removedirs as os_removedirs,
)
from unidecode import unidecode

from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from proplan.conf import (
    ATTACH_UPLOAD_PATH, ATTACH_THUMB_EXTENSIONS, PRIORITIES,
)


def upload_attach(instance, filename):
    filename = unidecode(filename).lower()
    filename = filename.replace(' ', '_').replace("'", '').replace('"', '')
    dic = {
        'filename': filename,
        'date': now().date().isoformat(),
        'code': get_random_string(),
        'user_id': instance.user_id or 0,
    }
    return ATTACH_UPLOAD_PATH % dic


class AttachmentManager(models.Manager):
    def get_free(self):
        qs = self.get_queryset()
        qs = qs.filter(thread__isnull=True, comment__isnull=True)
        return qs


class Attachment(models.Model):
    """Model of uploaded files."""

    created = models.DateTimeField(
        _('created'), auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        _('updated'), auto_now=True, db_index=True)
    # Who uploaded this file. The Automatic Bugs System sets as None.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('user'),
        related_name='proplan_attaches')
    file = models.FileField(_('file'), upload_to=upload_attach)

    objects = AttachmentManager()

    class Meta:
        verbose_name = _('attach')
        verbose_name_plural = _('attaches')
        ordering = ('-updated', '-created')

    def __str__(self):
        return self.file.path

    def delete(self, **kwargs):
        """Clears the directory of files before deleting the object."""
        if self.use_thumbnail:
            try:
                os_remove(self.thumb_path)
            except OSError:
                pass
        file = self.file
        path = file.path
        file.delete(False)
        try:
            os_removedirs(os_path.dirname(path))
        except OSError:
            pass
        super(Attachment, self).delete(**kwargs)

    @staticmethod
    def get_thumb_filename(filename):
        """Returns the name of the thumbnail created from the file name."""
        return '%s.thumb%s' % os_path.splitext(filename)

    @property
    def is_abs(self):
        """True if it uploaded from automatic bug system."""
        return not self.user_id

    @property
    def extension(self):
        """Returns extension for file in lower case."""
        root, ext = os_path.splitext(self.file.name)
        return ext.lower()

    @property
    def is_image(self):
        """Returns True if the file is an image."""
        L = (
            '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.svg',
        )
        return self.extension in L

    @property
    def use_thumbnail(self):
        """Returns True if the file is an image with thumbnail."""
        return self.extension in ATTACH_THUMB_EXTENSIONS

    @property
    def name(self):
        """Returns the cleaned name of file without path."""
        return os_path.basename(self.file.name)

    @property
    def url(self):
        return self.file.url

    @property
    def thumb_url(self):
        if self.use_thumbnail:
            return self.get_thumb_filename(self.file.url)
        return ''

    @property
    def path(self):
        return self.file.path

    @property
    def thumb_path(self):
        if self.use_thumbnail:
            return self.get_thumb_filename(self.file.path)
        return ''


class TrackerManager(models.Manager):
    def get_abs(self):
        qs = self.get_queryset()
        return qs.filter(is_abs=True).first()


class Tracker(models.Model):
    """
    Model of one tracker. By default exists 'idea', 'feature' and 'bug'.
    """
    name = models.CharField(_('name'), max_length=10, db_index=True)
    description = models.TextField(_('description'), blank=True)
    is_abs = models.BooleanField(
        _('for automatic bug system'), default=False,
        help_text=_('Only one record can be used for Automatic Bug System.'))

    objects = TrackerManager()

    class Meta:
        ordering = ('id',)
        verbose_name = _('tracker')
        verbose_name_plural = _('trackers')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super(Tracker, self).save(**kwargs)
        if self.is_abs:
            qs = Tracker.objects.filter(is_abs=True).exclude(id=self.id)
            qs.update(is_abs=False)


class StageManager(models.Manager):
    def get_abs(self):
        qs = self.get_queryset()
        return qs.filter(is_abs=True).first()


class Stage(models.Model):
    """
    Model of one stage. By default exists: 'new', 'discuss', 'develop',
    'testing', 'bugfix', 'finish' and 'reject'.
    """
    name = models.CharField(_('name'), max_length=10, db_index=True)
    description = models.TextField(_('description'), blank=True)
    # As example finished stages: "closed", "rejected", etc...
    is_finished = models.BooleanField(_('is finished'), default=False)
    is_abs = models.BooleanField(
        _('for automatic bug system'), default=False,
        help_text=_(
            'Only one record can be used for new stage for Automatic Bug '
            'System.'
        )
    )

    objects = StageManager()

    class Meta:
        ordering = ('id',)
        verbose_name = _('stage')
        verbose_name_plural = _('stages')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        # Can't be both as finished and as for ABS.
        if self.is_finished and self.is_abs:
            self.is_finished = False
        super(Stage, self).save(**kwargs)
        if self.is_abs:
            qs = Stage.objects.filter(is_abs=True).exclude(id=self.id)
            qs.update(is_abs=False)


class Role(models.Model):
    """
    Model of one user role.
    """
    name = models.CharField(_('name'), max_length=50, db_index=True)
    description = models.TextField(_('description'), blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, verbose_name=_('users'))
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
        related_name='proplan_roles',
        limit_choices_to={'content_type__app_label': 'proplan'},
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')

    def __str__(self):
        return self.name


class Thread(models.Model):
    """
    Model of one thread.
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    # Author of an idea or a bug found. The Automatic Bugs System sets as None.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('author'),
        related_name='proplan_author_threads',
    )
    # The parent thread.
    parent = models.ForeignKey(
        'Thread',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='children',
        verbose_name=_('parent thread'),
    )
    # Tracker is an idea, a bug or something else.
    tracker = models.ForeignKey(Tracker, verbose_name=_('tracker'),
                                on_delete=models.CASCADE)
    # The stage of current.
    stage = models.ForeignKey(Stage, verbose_name=_('stage'),
                              on_delete=models.CASCADE)
    # The higher the priority, the more important it is for the project.
    priority = models.SmallIntegerField(
        _('priority'), choices=PRIORITIES, default=1, db_index=True)
    # True if it received from automatic bug system.
    is_abs = models.BooleanField(
        _('from automatic bug system'), default=False, db_index=True)
    # Title of the thread.
    title = models.CharField(_('title'), max_length=255, db_index=True)
    # Detailed description of the thread.
    message = models.TextField(_('message body'), blank=True, db_index=True)
    # The files attached by the author of the thread.
    attachments = models.ManyToManyField(
        Attachment, blank=True, verbose_name=_('attachments'))

    class Meta:
        verbose_name = _('thread')
        verbose_name_plural = _('threads')
        ordering = ('-updated', '-created')

    def __str__(self):
        return self.title or 'new'

    @property
    def time_total(self):
        """Returns the seconds spended for total work."""
        qs = Executor.objects.filter(thread=self)
        seconds = sum([e.time_total for e in qs])
        return seconds

    @property
    def time_work(self):
        """Returns the seconds spended for work on sprints."""
        qs = Executor.objects.filter(thread=self)
        seconds = sum([e.time_work for e in qs])
        return seconds


class Comment(models.Model):
    """
    Model of one comment for thread.
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='proplan_comments',
    )
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, verbose_name=_('thread'))
    message = models.TextField(_('message body'), db_index=True)
    # JSON data about upgrading the thread.
    changes = models.TextField(_('thread changes'), blank=True, editable=False)
    attachments = models.ManyToManyField(
        Attachment, blank=True, verbose_name=_('attachments'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-updated', '-created')

    def __str__(self):
        return self.title


class Executor(models.Model):
    """
    Model of one executor for thread.
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    thread = models.ForeignKey(
        Thread,
        on_delete=models.PROTECT,
        related_name='executors',
        verbose_name=_('thread'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='proplan_executors',
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('user role'),
        related_name='executors',
    )
    # Start working on the thread.
    start = models.DateTimeField(
        _('start working'), null=True, blank=True, editable=False,
        db_index=True)
    # End working on the thread.
    stop = models.DateTimeField(
        _('stop working'), null=True, blank=True, editable=False,
        db_index=True)
    # The start time for the current sprint. This should be absent when there
    # is no work.
    sprint = models.DateTimeField(
        _('start of the sprint'), null=True, blank=True, editable=False)
    # The time of sprints in the seconds.
    time_sprints = models.IntegerField(
        _('time of the sprints'), default=0, editable=False, db_index=True)
    # The commentaries of the user between start and end work.
    comments = models.ManyToManyField(
        Comment, blank=True, verbose_name=_('comments'))

    class Meta:
        verbose_name = _('executor')
        verbose_name_plural = _('executors')
        ordering = ('-updated', '-created')
        permissions = (
            ('start_other_executor', _('Can start other executor')),
            ('stop_other_executor', _('Can stop other executor')),
        )

    def __str__(self):
        return '%s: %s' % (str(self.role), str(self.user))

    @property
    def time_total(self):
        """Returns the seconds spended for total work."""
        start = self.start
        stop = self.stop
        if start is None:
            return 0
        if stop is None:
            stop = now()
        return (stop - start).total_seconds()

    @property
    def time_work(self):
        """Returns the seconds spended for work on sprints."""
        time = self.time_sprints
        sprint = self.sprint
        if sprint:
            time += (now() - sprint).total_seconds()
        return time

    @property
    def is_current(self):
        return bool(self.sprint)

    def start_sprint(self, save=False):
        """Sets the start of the new sprint."""
        assert not self.sprint
        if not self.start:
            self.start = now()
        self.sprint = now()
        if save:
            self.save()
        return self.sprint

    def stop_sprint(self, save=False):
        """Stops the current sprint."""
        sprint = self.sprint
        assert sprint
        _now = now()
        time = (_now - sprint).total_seconds()
        self.time_sprints += time
        self.sprint = None
        self.stop = _now
        if save:
            self.save()
        return time
