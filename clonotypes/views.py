from django.shortcuts import render

def all(request, sample_id):
  return render(request, 'all.html')

