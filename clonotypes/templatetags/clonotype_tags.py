from django import template


register = template.Library()


@register.inclusion_tag('clonotype.html')
def clonotype_tag(clonotype):
    return {'clonotype': clonotype}
