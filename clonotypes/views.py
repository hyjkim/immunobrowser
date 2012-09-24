from django.shortcuts import render
from clonotypes.models import Clonotype
from samples.models import Sample

def all(request, sample_id):
  clonotypes = Clonotype.objects.all()
  sample = Sample.objects.get(id=sample_id)
  context = {'sample': sample, 'clonotypes':clonotypes}
  return render(request, 'all.html', context)

