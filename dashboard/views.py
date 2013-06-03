from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import simplejson as json
from patients.models import Patient
from samples.models import Sample

def add_samples(request):
    '''
    Processes an ajax request from the javascript menu, obtains the corresponding comparison
    and sends a template based html of the clonofilters in the comparison
    '''
    pass

def explorer(request):
    '''
    View for the hierarchical patient/sample selector.
    '''
#    context = {
#        'patients': Patient.objects.all(),
#    }
#    return render(request, 'explorer.html', context)
    return render(request, 'explorer.html')


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

#    dummy_data = [{'label': 'patient1',
#                  'children': [{'label':'child1',
#                                 'id':'s1',
#                               },
#                               {'label':'child2',
#                                'id': 's2',
#                                }
#                              ],
#                  'id': 'p1',
#                  },
#                  {'label': 'patient2',
#                   'id': 'p2',
#                  }
#                  ]
#
#    data = serializers.serialize('json', dummy_data)
#    data = json.dumps(dummy_data)
#    return HttpResponse(data, mimetype='application/json')
