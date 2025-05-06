from django import template

register = template.Library()

@register.filter
def nomes_grupos(user):
    return [g.name for g in user.groups.all()] 