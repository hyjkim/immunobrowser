from tastypie.resources import ModelResource
from tastypie import fields
from patients.models import Patient
from samples.models import Sample


class PatientResource(ModelResource):
    class Meta:
        queryset = Patient.objects.all()
        resource_name = 'patient'

class SampleResource(ModelResource):
    patient = fields.ForeignKey(PatientResource, 'patient')
    class Meta:
        queryset = Sample.objects.all()
        resource_name = 'sample'
