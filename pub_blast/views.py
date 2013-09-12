from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from pub_blast.forms import BlastForm
from pub_blast.models import BlastQuery


def new(request, **kwargs):
    '''
    View for generating a new blast query
    '''
    blast_form = BlastForm()
    if 'blast_form' in kwargs:
        blast_form = kwargs['blast_form']
    context = {'blast_form': blast_form}
    return render(request, 'new_pub_blast.html', context)

def submit(request):
    '''
    Takes a query in from post. Redirects to result page
    if submitted text is a valid fasta file
    '''
    try:
        blast_form = BlastForm(request.POST)
        if blast_form.is_valid():
            blast_query = BlastQuery.new_query(blast_form.cleaned_data['query'])
            return redirect(reverse('pub_blast.views.result', args=[blast_query.id]))
        else:
            context = {'blast_form': blast_form}
            return new(request, blast_form=blast_form)

    except Exception as e:
        print e
        return redirect(reverse('pub_blast.views.new'))

def result(request, query_id):
    return render(request, 'result.html', {})
