from django.shortcuts import render
from samples.models import Sample

def home(request):
  context = {'samples':Sample.objects.all()}
  return render(request, 'home.html', context)
