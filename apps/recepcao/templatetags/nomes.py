from django import template
register = template.Library()

@register.filter
def first_last(value):
    partes = value.split()
    if len(partes) == 1:
        return value
    return f"{partes[0]} {partes[-1]}" 