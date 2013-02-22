from django.shortcuts import render
from clonotypes.models import Clonotype
from samples.models import Sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def all(request, sample_id):
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
    context = {'sample': sample, 'clonotypes': clonotypes}
    return render(request, 'all.html', context)

def detail(request, clonotype_id):
    pass
#    try:
    clonotype = Clonotype.objects.get(id=clonotype_id)
    sample = clonotype.sample
    context = {'clonotype': clonotype, 'sample': sample}
    return render(request, 'detail.html', context)


