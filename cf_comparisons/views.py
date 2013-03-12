from django.shortcuts import render
from cf_comparisons.models import Comparison
from clonotypes.forms import ClonoFilterForm
from clonotypes.models import ClonoFilter

def compare(request, comparison_id):
    comparison = Comparison.objects.get(id=comparison_id)
    clonofilters = comparison.clonofilters.all()
    filter_forms = []
    for clonofilter in clonofilters:
        filter_forms.append(ClonoFilterForm(initial=ClonoFilter.objects.filter(id=clonofilter.id).values()[0]))

    context = {'filter_forms': filter_forms}
#    context = {'clonofilters': comparison.clonofilters.all()}
    return render(request, 'compare.html', context)
