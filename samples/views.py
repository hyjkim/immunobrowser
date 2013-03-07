from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from samples.models import Sample
from clonotypes.models import ClonoFilter
from clonotypes.forms import ClonoFilterForm


def home(request):
    context = {'samples': Sample.objects.all()}
    return render(request, 'home.html', context)


def summary(request, sample_id):
    s = Sample.objects.get(id=sample_id)

    if request.method == 'POST':  # Handling forms via POST
        cf_form = ClonoFilterForm(request.POST)
        if cf_form.is_valid():
            cf, created = ClonoFilter.objects.get_or_create(
                **cf_form.cleaned_data)
            url = "%s?clonofilter=%s" % (
                reverse('samples.views.summary', args=[s.id]), cf.id)
        else:
            url = reverse('samples.views.summary', args=[s.id])

        return HttpResponseRedirect(url)

    else:  # Nonforms via GET
        f = ClonoFilterForm(initial={'sample': s.id})
        cf = ClonoFilter(**{'sample': s})

        if 'clonofilter' in request.GET:
            cf_id = request.GET['clonofilter']
            try:
                cf = ClonoFilter.objects.get(id=cf_id)
                f = ClonoFilterForm(
                    initial=ClonoFilter.objects.filter(id=cf_id).values()[0])
            except:
                return HttpResponseRedirect(reverse('samples.views.summary', args=[s.id]))
        else:
            pass
        context = {'sample': s,
                   'filter_form': f,
                   'clonofilter': cf,
                   }
        return render(request, 'summary.html', context)
