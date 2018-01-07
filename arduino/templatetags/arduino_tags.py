import re
from django import template
from datetime import datetime
from django.utils.encoding import force_text

register = template.Library()


@register.filter(name="isEven")
def isEven(idProject):
    return idProject % 2


@register.filter(name="order_by")
def order_by(queryset, order):
    return queryset.order_by(order)


@register.filter(name="epoch2Date")
def epoch2Date(epoch):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(epoch)
    except ValueError:
        return "En proceso..."
    return datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')


@register.filter(name="decimalcomma")
def intdot(value):
    return value.replace(",", ".")


@register.filter(name="generatorcount")
def gencount(value):
    return len(list(value))
