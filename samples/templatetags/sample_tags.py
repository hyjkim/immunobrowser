from django import template


register = template.Library()


#@register.inclusion_tag('summary_tag.html')
#def sample_summary_tag(clonofilter_id):
#    return {'clonotype': clonotype}
