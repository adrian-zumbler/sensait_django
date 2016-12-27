from django import template
from datetime import datetime, time
from time import time, strftime
register = template.Library()


@register.filter(name="isEven")
def isEven(idProject):
    return idProject % 2


@register.filter(name="order_by")
def order_by(queryset, order):
    return queryset.order_by(order)


@register.filter(name="epochDate")
def epochDate(epoch):
    print epoch
    # return datetime.fromtimestamp(float(epoch)).strftime('%Y-%m-%d %H:%M:%S')
    # return datetime.utcfromtimestamp(float(epoch)).strftime('%Y-%m-%dT%H:%M:%SZ')
