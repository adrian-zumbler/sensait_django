from django import template
from datetime import datetime

register = template.Library()


@register.filter(name="isEven")
def isEven(idProject):
    return idProject % 2


@register.filter(name="order_by")
def order_by(queryset, order):
    return queryset.order_by(order)


@register.filter(name="epoch2Date")
def epoch2Date(epoch):
    print epoch
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(epoch)
    except ValueError:
        return "En proceso..."
    return datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
