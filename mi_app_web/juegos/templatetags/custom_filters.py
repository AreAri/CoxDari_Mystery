from django import template
from itertools import groupby as itertools_groupby
from operator import itemgetter

register = template.Library()

@register.filter
def agrupar_por(value, arg):
    grouped = itertools_groupby(sorted(value, key=itemgetter(arg)), itemgetter(arg))
    return [{'grouper': key, 'list': list(group)} for key, group in grouped]
