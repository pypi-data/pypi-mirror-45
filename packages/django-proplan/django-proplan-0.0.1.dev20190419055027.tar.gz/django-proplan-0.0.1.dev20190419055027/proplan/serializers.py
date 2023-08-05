#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.db.models import Model, Manager
from django.db.models.fields.files import FieldFile
from django.utils.encoding import force_text


def _instance_serializer(instance):
    return [
        instance.pk,
        force_text(instance),
    ]


class ObjectSerializer:
    """
    Serialize the fields of the object model.

    If the list of fields "only" is passed - it serializes only them if it is
    not present, then serializes all fields, except for the list "exclude".

    """
    model = None
    only = ()
    exclude = ()

    def __init__(self, model=None, only=None, exclude=None):
        if model is not None:
            self.model = model
        if only is not None:
            self.only = only
        elif exclude is not None:
            self.exclude = exclude
        self.is_ready = False
        if self.model:
            self.set_fields(self.model._meta)

    def __call__(self, instance, *args, **kwargs):
        return self.serialize(instance, *args, **kwargs)

    def set_fields(self, meta):
        # Collect all fields in the one heap.
        all = [f for f in meta.fields]
        if meta.many_to_many:
            all.extend([f for f in meta.many_to_many])
        # Make the list of needed fields.
        if self.only:
            list_fields = [f for f in all if f.name in self.only]
        elif self.exclude:
            list_fields = [f for f in all if f.name not in self.exclude]
        else:
            list_fields = all
        self.list_fields = list_fields
        self.is_ready = True
        return list_fields

    def serialize(self, instance, *args, **kwargs):
        """Full serialization the instance."""
        if not self.is_ready:
            self.set_fields(instance._meta)

        serializer = _instance_serializer
        result = {}
        fields = result

        for f in self.list_fields:
            name = f.name
            value = None
            data = getattr(instance, name, None)
            if isinstance(data, FieldFile):
                if data.name:
                    value = data.url
            elif isinstance(data, Model):
                value = serializer(data)
            elif isinstance(data, Manager):
                value = [serializer(i) for i in data.all()]
            else:
                value = data
            fields[name] = value
        return self.extend(instance=instance, data=result, *args, **kwargs)

    def extend(self, instance, data, *args, **kwargs):
        """The extension of the standard serialization."""
        return data


class ExecutorSerializer(ObjectSerializer):
    def extend(self, instance, data, *args, **kwargs):
        """The extension of the standard serialization."""
        data['time_total'] = instance.time_total
        data['time_work'] = instance.time_work
        data['is_current'] = instance.is_current
        return data


class ThreadSerializer(ObjectSerializer):
    def extend(self, instance, data, *args, **kwargs):
        """The extension of the standard serialization."""
        data['time_total'] = instance.time_total
        data['time_work'] = instance.time_work
        return data
