from django import template


register = template.Library()


@register.inclusion_tag('sample_compare_form.html')
def sample_compare_tag(sample_compare_form):
    return {'sample_compare_form': sample_compare_form}
