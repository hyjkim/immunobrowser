from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cf_comparisons.models import Comparison
from clonotypes.forms import ClonoFilterForm
from clonotypes.models import ClonoFilter


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
            comparison = Comparison.get_or_create_from_clonofilters(clonofilters)
        else:
            comparison = Comparison.objects.get(id=comparison_id)

            for cf_form in cf_forms:
                print cf_form.errors

        return HttpResponseRedirect(reverse('cf_comparisons.views.compare', args=[comparison.id]))

    comparison = Comparison.objects.get(id=comparison_id)
    clonofilters = comparison.clonofilters.all()
    filter_forms = []
    for index, clonofilter in enumerate(clonofilters):
        filter_forms.append(ClonoFilterForm(initial=ClonoFilter.objects.filter(
            id=clonofilter.id).values()[0], prefix=str(index)))

    context = {'filter_forms': filter_forms,
               'comparison': comparison,
               'num_forms': len(filter_forms),
               }
    return render(request, 'compare.html', context)


def bubble(request, comparison_id):
    '''
    Takes in a comparison id and generates a bubble plot such that
    each clonofilter within the comparison instance gets its own color
    '''
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from pylab import text, xlabel, ylabel

    comparison = Comparison.objects.get(id=comparison_id)
    response = HttpResponse(content_type='image/png')
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    x = []
    y = []
    color = []
    area = []

    # get a list of vj_counts
    vj_counts_list = [clonofilter.vj_counts()
                      for clonofilter in comparison.clonofilters.all()]

    for vj_counts in vj_counts_list:
        for v_index, list in enumerate(vj_counts):
            for j_index, counts in enumerate(list):
                x.append(v_index)
                y.append(j_index)
                color.append(counts)
                area.append(counts)

    sct = ax.scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)
    canvas.print_png(response)
    return response
