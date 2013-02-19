from django.shortcuts import render
from clonotypes.models import Clonotype
from samples.models import Sample


def all(request, sample_id):
    sample = Sample.objects.get(id=sample_id)
    clonotypes = Clonotype.objects.filter(sample=sample)
    context = {'sample': sample, 'clonotypes': clonotypes}
    return render(request, 'all.html', context)

