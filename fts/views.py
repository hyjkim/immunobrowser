from django.shortcuts import render

def qunit(request):
    ''' Serves a qunit view that inherits from the base so that
    tests and production code will use the same base '''
    return render (request, 'qunit.html')

