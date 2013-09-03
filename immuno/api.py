from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.utils import trailing_slash
from django.conf.urls import url
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import ClonoFilter
from cf_comparisons.models import Comparison


class PatientResource(ModelResource):
    class Meta:
        queryset = Patient.objects.all()
        resource_name = 'patient'

class SampleResource(ModelResource):
    patient = fields.ForeignKey(PatientResource, 'patient')
    class Meta:
        queryset = Sample.objects.all()
        resource_name = 'sample'

class ClonoFilterResource(ModelResource):
    class Meta:
        queryset = ClonoFilter.objects.all()
        resource_name = 'clonofilter'

class ComparisonResource(ModelResource):
    clonofilters = fields.ToManyField(ClonoFilterResource, 'clonofilters')
    class Meta:
        queryset = Comparison.objects.all()
        resource_name = 'comparison'

    # Expose certain model methods to tastypie api
    # http://stackoverflow.com/questions/14085865/exposing-model-method-with-tastypie
    def prepend_urls(self):
        """ Add the following array of urls to the ComparisonResource base urls """
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/vdj_freq%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('vdj_freq'), name="api_vdj_freq"),
        ]

    def vdj_freq(self, request, **kwargs):
         """ proxy for the comparions.vdj_freq method """
         # do a method check to avoid bad requests
         self.method_check(request, allowed=['get'])
         bundle = self.build_bundle(request=request)
         # using the primary key defined in the url, obtain the comparison
         comparison = self.cached_obj_get(
             bundle,
             **self.remove_api_resource_names(kwargs))
         # Return what the method output, tastypie will handle the serialization
         return self.create_response(request, comparison.vdj_freq())
