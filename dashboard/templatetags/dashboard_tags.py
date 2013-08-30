from django import template


register = template.Library()

@register.inclusion_tag('menu_tag.html')
def menu_tag():
    return {}
