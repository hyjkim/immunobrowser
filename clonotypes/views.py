from django.shortcuts import render
from clonotypes.models import Clonotype
from samples.models import Sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def all(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    clonotypes = Clonotype.objects.filter(sample=sample)
    context = {'sample': sample, 'clonotypes': clonotypes}
    return render(request, 'all.html', context)

def pagination(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    clonotypes = Clonotype.objects.filter(sample=sample)
    paginator = Paginator(clonotypes, 25)
    page = request.GET.get('page')

    try:
        clonotypes = paginator.page(page)
    except PageNotAnInteger:
        clonotypes = paginator.page(1)
    except EmptyPage:
        clonotypes = paginator.page(paginator.num_pages)

    return render(request, 'list.html',
                              {'clonotypes': clonotypes, 'sample': sample})
