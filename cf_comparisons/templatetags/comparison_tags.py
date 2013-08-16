from django import template


register = template.Library()


@register.inclusion_tag('sample_compare_form_tag.html')
def sample_compare_tag(sample_compare_form):
    return {'sample_compare_form': sample_compare_form}

@register.inclusion_tag('filter_forms_tag.html')
def filter_forms_tag(comparison):
    try:
        filter_forms = comparison.filter_forms_dict()
        num_forms = len(filter_forms.values())
        clonofilter_colors = comparison.colors()
        return {'filter_forms': filter_forms,
                'num_forms': num_forms,
               'sample_colors': clonofilter_colors,
                }
    except Exception as e:
        print e
        return {}

@register.inclusion_tag('compare_ajax_tag.html')
def comparison_tag(comparison):
    samples = comparison.get_samples()
    shared_amino_acids = comparison.get_shared_amino_acids_related()
    context = {
               'comparison': comparison,
               'samples': samples,
               'shared_amino_acids': shared_amino_acids,
               }

    return context

@register.inclusion_tag('scatter_nav.html')
def scatter_nav_tag(comparison):
    pass

