from django import template
import json


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
#        print e
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

@register.inclusion_tag('scatter_nav_tag.html')
def scatter_nav_tag(comparison):
    from clonotypes.models import Recombination
    import json
    clonofilters = sorted(comparison.clonofilters.all())
    vj_counts_dict_dict= dict([(clonofilter.id, clonofilter.vj_counts_dict())
                      for clonofilter in clonofilters])

    v_list = sorted(Recombination.v_family_names())
    j_list = sorted(Recombination.j_gene_names())

    data = []

    # Counts for the scatter plot
    for clonofilter_id, vj_counts_dict in vj_counts_dict_dict.iteritems():
        for v_index, v_family in enumerate(v_list):
            for j_index, j_gene in enumerate(j_list):
                data_point = []
                data_point.append(v_list[v_index])
                data_point.append(j_list[j_index])
                if vj_counts_dict[v_family][j_gene]:
                    data_point.append(vj_counts_dict[v_family][j_gene])
                else:
                    data_point.append(0)
                # Append sample id
                data_point.append(clonofilter_id);
                if data_point[2] > 0:
                    data.append(data_point)

    # Functionality stats
    comp_functionality = []
    for cf in clonofilters:
        cf_functionality = {}
        values = {}
        for key, value in cf.functionality_dict().iteritems():
            values[key] = value
        cf_functionality['key'] = cf.id
        cf_functionality['values'] = values
        comp_functionality.append(cf_functionality)

    context = {'data': json.dumps(data),
               'v_list': json.dumps(v_list),
               'j_list': json.dumps(j_list),
               'sample_names': json.dumps(comparison.sample_names()),
               'sample_colors': json.dumps(comparison.colors()),
               'comparison_id': comparison.id,
               'functionality': json.dumps(comp_functionality),
               }

    return context


@register.inclusion_tag('shared_clones_tag.html')
def shared_clones_tag(comparison):
    import json
    shared_amino_acids_counts = comparison.get_shared_amino_acids_counts()
    context = {
               'amino_acids': shared_amino_acids_counts,
               'sample_names': comparison.sample_names(),
               'sample_colors': json.dumps(comparison.colors()),
            }
    return context

