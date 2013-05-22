from django.shortcuts import render


def explorer(request):
    '''
    View for the hierarchical patient/sample selector.
    '''
    from patients.models import Patient
    context = {
            'patients': Patient.objects.all(),
            }
    return render(request, 'explorer.html', context)
