#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from functools import reduce
from operator import or_ as OR
from PIL import Image, ImageOps

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Q, CharField
from django.shortcuts import _get_queryset
# from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from proplan.models import Attachment, Thread
from proplan.conf import ATTACH_THUMB_SIZE
from proplan.serializers import ObjectSerializer


User = get_user_model()


def create_attachment(user, file):
    """Creats the attachment file."""
    if user:
        assert isinstance(user, (User, AnonymousUser)), (
            'Parameter "user" is not valid.')
        if user.is_anonymous:
            user = None
    assert file and hasattr(file, 'content_type'), (
        'Parameter "file" is not valid.')
    name = file.name
    assert '.' in name, 'File not contain extension'
    assert '/' not in name, 'File contain slash'
    attachment = Attachment(user=user, file=file)
    attachment.full_clean()
    attachment.save()
    if attachment.use_thumbnail:
        try:
            with Image.open(attachment.path) as image:
                thumb = ImageOps.fit(image, ATTACH_THUMB_SIZE, Image.ANTIALIAS)
                # Save the thumbnail.
                thumb.save(attachment.thumb_path, 'png')
        except OSError as e:
            attachment.delete()
            raise TypeError(
                _('The image attachment is incorrect format.')
            )
    return attachment


def similarity_checking(title, message, is_abs=False, tracker=None,
                        exclude_id=None):
    qs = Thread.objects.all()
    qs = qs.none()
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    return list(qs.values_list('id', flat=True))


class Controller:
    """
    Filtering, ordering and pagination controller for QuerySet.
    """
    search_fields = None
    ordering_fields = None
    filtering_fields = None
    exclude_fields = ('password',)
    serializer = None

    def __init__(self, model, serializer=None):
        self.model = model
        meta = model._meta
        exclude = self.exclude_fields
        fields = [f for f in meta.fields if f.name not in exclude]
        if meta.many_to_many:
            fields.extend([
                f for f in meta.many_to_many if f.name not in exclude
            ])
        self.fields = fields
        if self.serializer is None:
            self.serializer = (
                serializer or ObjectSerializer(model=model, exclude=exclude)
            )
        if isinstance(self.serializer, type):
            self.serializer = self.serializer(model=model, exclude=exclude)

    def get_queryset(self):
        return _get_queryset(self.model)

    def get_search_fields(self):
        if self.search_fields is None:
            fields = [f.name for f in self.fields if isinstance(f, CharField)]
            # Search by models without text fields.
            if not fields:
                exclude = self.exclude_fields
                for field in self.fields:
                    rel = field.related_model
                    if rel:
                        prefix = field.name + '__%s'
                        for f in rel._meta.fields:
                            if isinstance(f, CharField):
                                fname = prefix % f.name
                                if fname not in exclude:
                                    fields.append(fname)
            self.search_fields = fields
        return self.search_fields

    def get_ordering_fields(self):
        if self.ordering_fields is None:
            self.ordering_fields = [f.name for f in self.fields if
                                    not f.related_model]
        return self.ordering_fields

    def get_filtering_fields(self):
        if self.filtering_fields is None:
            self.filtering_fields = [f.name for f in self.fields]
        return self.filtering_fields

    def ordering(self, queryset, ordering):
        """
        The function checks the collation and applies only the valid.
        """
        fields = self.get_ordering_fields()

        if not ordering or not fields:
            # Fix UnorderedObjectListWarning:
            if not getattr(queryset, 'ordered', True):
                queryset = queryset.order_by('pk')
            return queryset

        def valid(x):
            return bool(
                x and not x.startswith('--') and
                x.lstrip('-') in fields
            )

        if isinstance(ordering, str):
            if ordering.startswith('[') and ordering.endswith(']'):
                ordering = ordering[1:-1]
            ordering = ordering.split(',')
        ordering = [x for x in ordering if valid(x)]
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset, ordering

    def search(self, queryset, query):
        """
        Returns a filtered set of data.

        Parameter `klass` may be Model, Manager or QuerySet object. If there
        is no list of fields 'fields' or there is no search string 'query',
        then returns the data set as is.
        """

        fields = self.get_search_fields()

        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        if fields:
            lookups = [construct_search(str(f)) for f in fields]
            if query not in ('', None, False, True):
                for bit in query.split():
                    queries = [Q(**{lookup: bit}) for lookup in lookups]
                    queryset = queryset.filter(reduce(OR, queries))

        return queryset

    def filtering(self, queryset, filters):
        """Filters the queryset."""

        if not filters:
            return queryset, {}

        fields = self.get_filtering_fields()

        def test_filtered(field):
            for f in fields:
                if field.startswith(f):
                    return True
            return False

        def test_inverse(s):
            return s.startswith('-')

        def test_bool(s, v):
            return s.endswith('__isnull') or v in ('true', 'false')

        def test_list(s):
            return s.endswith('__in') or s.endswith('__range')

        applied = {}

        for field, query in filters.items():
            if field == 'q':
                queryset = self.search(queryset, query)
                applied[field] = query
                continue

            if test_inverse(field):
                field = field[1:]
                func = queryset.exclude
            else:
                func = queryset.filter

            if not test_filtered(field):
                continue

            if isinstance(query, str):
                if query.startswith('[') and query.endswith(']'):
                    query = [x for x in query[1:-1].split(',') if x]
                elif test_list(field):
                    query = [x for x in query.split(',') if x]
                elif test_bool(field, query):
                    query = bool(query == 'true')
            queryset = func(Q(**{field: query}))
            applied[field] = query

        return queryset, applied

    def pagination(self, queryset, limit, page):
        """Returns paginator and page for queryset."""
        paginator = Paginator(queryset, limit)
        try:
            page = paginator.page(page)
        except paginator.EmptyPage:
            page = paginator.page(1)
        return paginator, page

    def get(self, request, queryset=None, page=1, limit=100, max_limit=1000):
        """
        Prepares the request and returns page, orders and filters.
        """
        data = request.GET.copy()
        if queryset is None:
            queryset = self.get_queryset()
        else:
            assert self.model == queryset.model
        if 'p' in data:
            try:
                page = int(data.pop('p'))
            except ValueError:
                pass
        if 'l' in data:
            try:
                limit = int(data.pop('l'))
            except ValueError:
                pass
        if limit > max_limit:
            limit = max_limit
        if 'o' in data:
            queryset, orders = self.ordering(queryset, data.pop('o'))
        else:
            orders = []
        queryset, filters = self.filtering(queryset, data)
        paginator, page = self.pagination(queryset, limit, page)
        return page, orders, filters

    def get_serialized(self, *args, **kwargs):
        serializer = kwargs.pop('serializer', None)
        page, orders, filters = self.get(*args, **kwargs)
        page = self.serialize_page(page, serializer)
        return page, orders, filters

    def serialize_page(self, page, serializer):
        if serializer is None:
            serializer = self.serializer
        paginator = page.paginator
        return {
            'objects': [serializer(obj) for obj in page.object_list],
            'number': page.number,
            'limit': paginator.per_page,
            'count': paginator.count,
            'pages': paginator.num_pages,
        }
