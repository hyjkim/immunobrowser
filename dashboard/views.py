from django.shortcuts import render
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json
from patients.models import Patient
from samples.models import Sample
from cf_comparisons.models import Comparison
from dashboard.forms import SearchForm


def search(request):
    '''
    Reads a search term in from uri (via get or urlrouter) and returns
    a rendered page containing search results
    '''
    from clonotypes.models import Recombination, AminoAcid
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    context = {}
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            # Get search terms
            terms = search_form.cleaned_data['query'].split(' ')

            # Generate queryset
            recs = Recombination.objects.search(terms)
            aas = AminoAcid.objects.search(terms)

            # Paginate the querysets
            rec_paginator = Paginator(recs, 10)
            aa_paginator = Paginator(aas, 10)

            # Get page numbers
            rec_page = request.GET.get('rec_page')
            aa_page = request.GET.get('aa_page')

            try:
                recs = rec_paginator.page(aa_page)
            except PageNotAnInteger:
                recs = rec_paginator.page(1)
            except EmptyPage:
                recs = rec_paginator.page(recs_paginator.num_pages)

            try:
                aas = aa_paginator.page(aa_page)
            except PageNotAnInteger:
                aas = aa_paginator.page(1)
            except EmptyPage:
                aas = aa_paginator.page(aas_paginator.num_pages)


            context.update({'samples': Sample.objects.search(terms),
                'recombinations': recs,
                'amino_acids': aas,
                })
    else:
        search_form = SearchForm()

    context.update({'search_form': search_form})

    return render(request, 'search.html', context)

def remove_clonofilter(request):
    '''
    Given a comparison id and a clonofilter id from post
    get or create a comparison without the specified clonofilter.
    Returns updated comparison id via http response.
    '''
    if request.method == "POST":
        comp = Comparison.objects.get(id=request.POST['comparison'])
        cfs = [cf.id for cf in comp.clonofilters.all() if cf.id != int(request.POST['clonofilter'])]
        new_comp, created = Comparison.get_or_create_from_clonofilters(cfs)
        return HttpResponse(new_comp.id)
    else:
        return HttpResponseRedirect(reverse('dashboard.views.compare_v2'))

def add_samples_v2(request):
    '''
    Processes an ajax request.
    Given an array of sampleId's, returns an array of
    clonofilter forms. The clonofilter forms are then
    submitted to generate a new comparison id which is
    used to generate all interactive dataplots.
    '''
    if request.method  == "POST":
        sample_ids = [int(i) for i in request.POST.getlist('samples')]
        samples = Sample.objects.filter(id__in=sample_ids)
        # See if there is an existing sample
        try:
            old_comparison = Comparison.objects.get(id=request.POST['comparison'])
            comparison = old_comparison.add_samples(samples)
        except:
            comparison = Comparison.default_from_samples(samples)

        return HttpResponse(comparison.id)
    else:
        return HttpResponseRedirect(reverse('dashboard.views.compare_v2'))

def home(request):
    context = {}
    return render(request, 'home.html', context)

def compare_v2(request, comparison_id):
    '''
    version 2 of the explorer
    '''
    from cf_comparisons.forms import SampleCompareForm

    sample_compare_form = SampleCompareForm()
    search_form = SearchForm()

    try:
        comparison = Comparison.objects.get(id=comparison_id)
    except:
        comparison=None

    context = {'sample_compare_form': sample_compare_form,
            'search_form': search_form,
            'comparison': comparison,
            }

    return render(request, 'compare_v2.html', context)

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
