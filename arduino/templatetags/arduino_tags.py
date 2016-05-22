from django import template
register = template.Library()

@register.filter(name="isEven")
def isEven(idProject):
    return idProject%2
