from django.shortcuts import render
from samples.models import Sample

def home(request):
  context = {'samples':Sample.objects.all()}
  return render(request, 'home.html', context)

def summary(request, sample_id):
  context = {'sample':Sample.objects.get(id=sample_id)}
  return render(request, 'summary.html', context)
