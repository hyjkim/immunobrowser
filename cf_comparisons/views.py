from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cf_comparisons.models import Comparison
from clonotypes.forms import ClonoFilterForm
from clonotypes.models import ClonoFilter


def update(request, comparison_id):
    '''
    Given a comparison id parsed from the url and an
    update dict via post, returns the id of a new
    comparison for JSON requests
    '''
    import json
    comparison = Comparison.objects.get(id=comparison_id)
    if request.method == "POST":
        update_dict = json.loads(request.POST['update'])
        update_dict = dict((int(k), v) for (k,v) in update_dict.iteritems())
        new_comp = comparison.update(update_dict)
    return HttpResponse(new_comp.id, content_type="application/json")


def d3_test(request, comparison_id):
    '''
    This is a test of the d3 library.
    '''
    from clonotypes.models import Recombination
    from django.utils import simplejson as json
    from matplotlib.colors import rgb2hex
    comparison = Comparison.objects.get(id=comparison_id)
    clonofilters = sorted(comparison.clonofilters.all())
    sample_names = dict([(clonofilter.id,str(clonofilter.sample)) for clonofilter in clonofilters])
    vj_counts_dict_dict= dict([(clonofilter.id, clonofilter.vj_counts_dict())
                      for clonofilter in clonofilters])
    clonofilter_colors = comparison.colors()

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
               'sample_names': json.dumps(sample_names),
               'sample_colors': json.dumps(clonofilter_colors),
               'comparison_id': comparison_id,
               'functionality': json.dumps(comp_functionality),
               }

    return render(request, 'd3_test.html', context)

def sample_compare(request):
    from cf_comparisons.forms import SampleCompareForm

    if request.method == 'POST':
        sample_compare_form = SampleCompareForm(request.POST)
        if sample_compare_form.is_valid():
            comparison = Comparison.default_from_samples(
                sample_compare_form.cleaned_data['samples'])
            return HttpResponseRedirect(reverse('cf_comparisons.views.compare', args=[comparison.id]))

    sample_compare_form = SampleCompareForm()
    context = {'sample_compare_form': sample_compare_form}
    return render(request, 'sample_compare.html', context)

def filter_forms(request, comparison_id):
    '''
    Filter forms are served directly from the compare template
    if the request is not ajax. Ajax requests don't include
    the filter forms. This view, generates the filter form markup
    and returns it so that a jquery operation can fill it into the
    appropriate place
    '''
    from django.template import Template, Context
    comparison = Comparison.objects.get(id=comparison_id)
#    template = Template('{% load comparison_tags %}{% filter_forms_tag filter_forms %}')
    context = Context({'comparison': comparison})
    return render(request, 'filter_forms.html', context)

#    return HttpResponse(template.render(context))

def compare(request, comparison_id):
    '''
    Compare view takes in a comparison object and generates a summary view
    that compares an arbitrary number of clonofilters
    '''

    if request.method == 'POST':
        num_forms = int(request.POST['num_forms'])

        cf_forms = [ClonoFilterForm(request.POST, prefix=str(x))
                    for x in range(0, num_forms)]
        if all([cf_form.is_valid() for cf_form in cf_forms]):
            clonofilters = []
            for cf_form in cf_forms:
                cf, created = ClonoFilter.objects.get_or_create(
                    **cf_form.cleaned_data)
                clonofilters.append(cf)
            comparison, created = Comparison.get_or_create_from_clonofilters(clonofilters)
        else:
            comparison = Comparison.objects.get(id=comparison_id)

            for cf_form in cf_forms:
                print cf_form.errors

        return HttpResponseRedirect(reverse('cf_comparisons.views.compare', args=[comparison.id]))

    comparison = Comparison.objects.get(id=comparison_id)
    filter_forms = comparison.filter_forms_list()


    shared_amino_acids = comparison.get_shared_amino_acids_related()

    samples = comparison.get_samples()
    context = {
               'comparison': comparison,
               'samples': samples,
               'shared_amino_acids': shared_amino_acids,
               }

    if request.is_ajax():
        return render(request, 'compare_ajax.html', context)
    else:
        context.update({'filter_forms': filter_forms})
        return render(request, 'compare.html', context)

def spectratype(request, comparison_id):
    '''
    Takes in a comparison id and generates a combined spectratype.

    This spectratype should also plot an average spectratype with +/-
    one standard deviation.
    '''
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from numpy import array
    from collections import defaultdict

    # Init various stuffs
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    comp = Comparison.objects.get(id=comparison_id)
    color_dict = comp.colors_dict()
    legend_items = []
    legend_labels = []

    # Generate cdr3 sums for each clonofilter
    for clonofilter, color in color_dict.items():
        cdr3_sums = array(clonofilter.cdr3_length_sum())
        ax.plot(cdr3_sums[:, 0].tolist(), cdr3_sums[:, 1].tolist(), '-', color=color)
        # Used in generating the legend
        legend_items.append(plt.Line2D(range(1), range(1) ,color=color))
        legend_labels.append(str(clonofilter.sample))

    # Get average cdr3 sums
    average = defaultdict(lambda: 0)
    for clonofilter in comp.clonofilters.all():
        cdr3_sums = array(clonofilter.cdr3_length_sum())
        for x, y in cdr3_sums:
            average[x] += y

    # scale the average
    averaged_values = array(average.values()) / len(comp.clonofilters.all())
    ax.plot(average.keys(), averaged_values, color="grey")



    # Axes labels and title
    ax.set_title('%s Spectratype' % clonofilter.sample)
    ax.set_xlabel('CDR3 Length (Nucleotides)')
    ax.set_ylabel('Usage')

    # legend time
    ax.legend(legend_items, legend_labels)


    # print and return reponse
    canvas.print_png(response)
    return response

def bubble(request, comparison_id):
    '''
    Takes in a comparison id and generates a bubble plot such that
    each clonofilter within the comparison instance gets its own color
    '''
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    from clonotypes.models import Recombination
    from math import sqrt
    import pylab
    import numpy as np

    comparison = Comparison.objects.get(id=comparison_id)
    clonofilters = sorted(comparison.clonofilters.all())
    response = HttpResponse(content_type='image/png')
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    clonofilter_colors = comparison.colors_list()

    x = []
    y = []
    color = []
    data = []
    area = []

    # Calculate the plotting area by finding the number of v's and j's
    v_list = sorted(Recombination.v_family_names())
    j_list = sorted(Recombination.j_gene_names())
    width = len(v_list)
    height = len(j_list)

    # get a list of vj_counts
    vj_counts_dict_list = [clonofilter.vj_counts_dict()
                      for clonofilter in clonofilters]

    for clonofilter_index, vj_counts_dict in enumerate(vj_counts_dict_list):
        for v_index, v_family in enumerate(v_list):
            for j_index, j_gene in enumerate(j_list):
                x.append(v_index)
                y.append(j_index)
                color.append(clonofilter_colors[clonofilter_index])
                if vj_counts_dict[v_family][j_gene]:
                    data.append(vj_counts_dict[v_family][j_gene])
                else:
                    data.append(0)


    # Normalize area by the median and plot area
    #area_norm_factor = (1.0/median(data)) * width * height

    if data:
        area_norm_factor = (2.0/max(data)) * width * height
        area = [datapoint * area_norm_factor for datapoint in data]

    sct = ax.scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.4)

# Labels, legends, titles etc
    # Set titles
    ax.set_title('V-J Usage Comparison')
    ax.set_xlabel('V Gene Family')
    ax.set_ylabel('J Gene')
    # Add a grid
    ax.yaxis.grid(True, linestyle='-', which='both', color='lightgrey',
                  alpha=0.5)
    ax.xaxis.grid(True, linestyle='-', which='both', color='lightgrey',
                  alpha=0.5)

    # Set the axes and plotting area
    ax.set_xlim(-1, width)
    ax.set_ylim(-1, height)
    xtickNames = plt.setp(ax, xticklabels=v_list)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    ax.xaxis.set_ticks(range(len(v_list)))
    ytickNames = plt.setp(ax, yticklabels=j_list)
    plt.setp(ytickNames, fontsize=9)
    ax.yaxis.set_ticks(range(len(j_list)))

    # Shrink the plot to make room for legends
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Draw the bubble size legend
    max_data = max(data)
    bubbles = []
    bubble_labels = []

    # Labels for exponentially decreasing bubble sizes
    for bubble_area in [max_data * 1.45 ** (-exp) for exp in range(0, 10)]:
        # Determine marker size
        marker_size = sqrt(
            bubble_area / max_data * (len(j_list) * len(v_list * 2)))
        marker_color = 'lightgrey'
        bubbles.append(plt.Line2D(range(1), range(1), marker='o', markersize=marker_size, color=marker_color, linewidth=0, markeredgecolor="lightgrey", alpha=0.5))
        bubble_labels.append('%g' % bubble_area)

    # Labels for sample colors
    for index, clonofilter in enumerate(clonofilters):
        marker_size = sqrt(width * height/ 1.5)
        marker_color = clonofilter_colors[index]
        bubbles.append(plt.Line2D(range(1), range(1), marker='o', markersize=marker_size, color=marker_color, linewidth=0, markeredgecolor="lightgrey", alpha=0.5))
        bubble_labels.append('%s' % clonofilter.sample)


    ax.legend(bubbles, bubble_labels, numpoints=1, loc='center left', bbox_to_anchor=(1., .5), labelspacing=1.5, prop={'size': 10}, title="Counts")

    canvas.print_png(response)
    return response
