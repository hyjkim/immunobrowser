from django import template


register = template.Library()


@register.inclusion_tag('sample_compare_form.html')
def sample_compare_tag(sample_compare_form):
    return {'sample_compare_form': sample_compare_form}

@register.inclusion_tag('filter_forms.html')
def filter_forms_tag(filter_forms):
    num_forms = len(filter_forms)
    return {'filter_forms': filter_forms,
            'num_forms': num_forms}
