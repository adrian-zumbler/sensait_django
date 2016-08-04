from django import template
register = template.Library()

@register.filter(name="isEven")
def isEven(idProject):
    return idProject%2


@register.filter(name="order_by")
def order_by(queryset, order):
    return queryset.order_by(order)
