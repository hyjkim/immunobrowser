from django import template


register = template.Library()


@register.inclusion_tag('clonofilter_summary.html')
def clonofilter_summary_tag(clonofilter):
    return {'clonofilter': clonofilter}
