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

@register.inclusion_tag('compare_ajax.html')
def comparison_tag(comparison):
    samples = comparison.get_samples()
    shared_amino_acids = comparison.get_shared_amino_acids_related()
    context = {
               'comparison': comparison,
               'samples': samples,
               'shared_amino_acids': shared_amino_acids,
               }

    return context
