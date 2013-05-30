from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import simplejson as json
from patients.models import Patient

def explorer(request):
    '''
    View for the hierarchical patient/sample selector.
    '''
    context = {
        'patients': Patient.objects.all(),
    }
    return render(request, 'explorer.html', context)


def menu_json(request):
    '''
    returns a serialized json object of all patients and samples
    '''
    dummy_data = [{'label': 'patient1',
                  'children': [{'label':'child1',
                                 'id':'s1',
                               },
                               {'label':'child2',
                                'id': 's2',
                                }
                              ],
                  'id': 'p1',
                  },
                  {'label': 'patient2',
                   'id': 'p2',
                  }
                  ]

#    data = serializers.serialize('json', dummy_data)
    data = json.dumps(dummy_data)
    return HttpResponse(data, mimetype='application/json')
