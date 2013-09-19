from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lit_search.forms import BlatForm
from lit_search.models import BlatQuery


def new(request, **kwargs):
    '''
    View for generating a new blat query
    '''
    blat_form = BlatForm()
    if 'blat_form' in kwargs:
        blat_form = kwargs['blat_form']
    context = {'blat_form': blat_form}
    return render(request, 'new_pub_blat.html', context)

def submit(request):
    '''
    Takes a query in from post. Redirects to result page
    if submitted text is a valid fasta file
    '''
    try:
        blat_form = BlatForm(request.POST)
        if blat_form.is_valid():
            blat_query = BlatQuery.new_query(blat_form.cleaned_data['query'])
            return redirect(reverse('lit_search.views.result', args=[blat_query.id]))
        else:
            context = {'blat_form': blat_form}
            return new(request, blat_form=blat_form)

    except Exception as e:
        print e
        return redirect(reverse('lit_search.views.new'))

def result(request, query_id):
    '''
    Happy path for results. Checks to see if the celery
    task has completed and if so, returns the blat result
    '''
    try:
        blat_query = BlatQuery.objects.get(id=query_id)
        context = {'blat_query': blat_query}
        if blat_query.ready():
            return render(request, 'result.html', context)
        else:
            return render(request, 'processing.html',context)
    except Exception as e:
        print e
        return result_not_found(request)


def result_not_found(request):
    '''
    sad path for blat queries that aren't found in db
    '''
    return render(request, 'result_not_found.html')
