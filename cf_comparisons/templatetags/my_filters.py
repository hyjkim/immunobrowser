# my_filters.py
# Some custom filters for dictionary lookup.
from django.template.defaultfilters import register
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''


@register.filter(name='jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

jsonify.is_safe = True
