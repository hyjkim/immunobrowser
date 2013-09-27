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


def help(request):
    '''
    A static view that is used to describe TCR-receptor sequencing technology,
    its applications and describes the utility of the immunobrowser
    '''
    return render (request, 'help.html', {})

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
                recs = rec_paginator.page(rec_page)
            except PageNotAnInteger:
                recs = rec_paginator.page(1)
            except EmptyPage:
                recs = rec_paginator.page(rec_paginator.num_pages)

            try:
                aas = aa_paginator.page(aa_page)
            except PageNotAnInteger:
                aas = aa_paginator.page(1)
            except EmptyPage:
                aas = aa_paginator.page(aa_paginator.num_pages)


            context.update({'samples': Sample.objects.search(terms),
                'recombinations': recs,
                'amino_acids': aas,
                'terms': '+'.join(terms),
                })
    else:
        search_form = SearchForm()

    context.update({'search_form': search_form})

    return render(request, 'search.html', context)

def home(request):
    context = {}
    return render(request, 'home.html', context)
