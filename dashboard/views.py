from django.shortcuts import render
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json
from patients.models import Patient
from samples.models import Sample
from cf_comparisons.models import Comparison

def add_samples(request):
    '''
    Processes an ajax request from the javascript menu, obtains the corresponding comparison
    and sends a template based html of the clonofilters in the comparison
    '''
    sample_ids = json.loads(request.POST['sample_ids'])
    samples = Sample.objects.filter(id__in=sample_ids)
    comparison = Comparison.default_from_samples(samples)

#    return HttpResponseRedirect(reverse('cf_comparisons.views.compare', args=[comparison.id]))
    return HttpResponse(comparison.id)

def dashboard_comparison(request, comparison_id):
    comparison = Comparison.objects.get(id=comparison_id)
    context = {
               'comparison': comparison
              }
    return render(request, 'dashboard_comparison.html', context)

def dashboard_v2(request):
    '''
    version 2 of the explorer
    '''
    from cf_comparisons.forms import SampleCompareForm

    sample_compare_form = SampleCompareForm()
    context = {'sample_compare_form': sample_compare_form}

    return render(request, 'dashboard_v2.html', context)

@ensure_csrf_cookie
def explorer(request):
    '''
    View for the hierarchical patient/sample selector.
    '''
    context = {
        'patients': Patient.objects.all(),
   }
    return render(request, 'explorer.html', context)
#    return render(request, 'explorer.html')


def menu_json(request):
    '''
    returns a serialized json object of all patients and samples
    '''
    data = []
    for patient in Patient.objects.all():
        patient_dict = {}
        patient_dict['label'] = str(patient)
        patient_dict['id'] = "patient_%s" % (patient.id)
        samples = patient.sample_set.all()
        if (len(samples) > 0):
            patient_dict['children'] = []
            for sample in samples:
                sample_dict = {}
                sample_dict['label'] = str(sample)
                sample_dict['id'] = 'sample_%s' % (sample.id)
                sample_dict['pk'] = sample.id
                patient_dict['children'].append(sample_dict)
        data.append(patient_dict)

    return HttpResponse(json.dumps(data), mimetype='application/json')
