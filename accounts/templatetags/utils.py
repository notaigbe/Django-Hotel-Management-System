import json

from django import template
from django.utils.safestring import mark_safe
from django.core import serializers
from django.utils.encoding import is_protected_type
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()


@register.filter
def queryset_as_json(qs):
    """
    Sample usage:
        {{user.list_tipi_movimento|queryset_as_json}}
    """
    json_data = serializers.serialize("json", qs)
    return mark_safe(json_data)


def object_as_dict(obj):
    data = {}

    for field in obj._meta.local_fields:
        # Code stolen from Serializer
        value = field.value_from_object(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            data[field.name] = value
        else:
            data[field.name] = field.value_to_string(obj)

    # Collect ids of M2M related items
    for field in obj._meta.get_fields():
        if field.is_relation and field.many_to_many:
            data[field.name] = [str(o.id) for o in getattr(obj, field.name).all()]

    return data


@register.filter
def object_as_json(obj):
    """
    Sample usage:
        {{original|object_as_json}}
    """

    try:
        data = object_as_dict(obj)
    except:
        data = {}

    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    return mark_safe(json_data)
