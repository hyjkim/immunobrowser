from django.shortcuts import render
# Create your views here.

def patient_summary(request, patient_id):
    '''
    Patient summary view shows all samples from the patient
    '''
    context = {}
    return render(request, 'patient_summary.html', context)
