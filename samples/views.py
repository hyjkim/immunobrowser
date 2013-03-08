from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from samples.models import Sample
from clonotypes.models import ClonoFilter
from clonotypes.forms import ClonoFilterForm
from django.forms.models import model_to_dict


def home(request):
    context = {'samples': Sample.objects.all()}
    return render(request, 'home.html', context)


def summary(request, sample_id):
    ''' summary takes in a request and a sample id and
    displays an array of summary images and statistics.
    It can also take a clonofilter via POST or GET
    '''
    s = Sample.objects.get(id=sample_id)

    if request.method == 'POST':  # Handling changes to filter form via POST
        cf_form = ClonoFilterForm(request.POST)
        if cf_form.is_valid():
            cf, created = ClonoFilter.objects.get_or_create(
                **cf_form.cleaned_data)
            url = "%s?clonofilter=%s" % (
                reverse('samples.views.summary', args=[s.id]), cf.id)
        else:
            url = reverse('samples.views.summary', args=[s.id])

        return HttpResponseRedirect(url)

    else:  # Handling requests via GET
        f = ClonoFilterForm(initial={'sample': s.id})
        cf = ClonoFilter(**{'sample': s})
        cf_dict = model_to_dict(cf)
        cf_dict['sample'] = s

        cf, created = ClonoFilter.objects.get_or_create(**cf_dict)

        # Sets up the form to reflect the clonofilter supplied by GET
        if 'clonofilter' in request.GET:
            cf_id = request.GET['clonofilter']
            try:
                cf = ClonoFilter.objects.get(id=cf_id)
                f = ClonoFilterForm(
                    initial=ClonoFilter.objects.filter(id=cf_id).values()[0])
#            except Exception as e:
#                print e
            except:
                return HttpResponseRedirect(reverse('samples.views.summary', args=[s.id]))
        else:
            pass
        context = {'sample': s,
                   'filter_form': f,
                   'clonofilter': cf,
                   }
        return render(request, 'summary.html', context)
