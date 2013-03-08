from django import forms
#from samples.models import Sample
from clonotypes.models import ClonoFilter


#class ClonoFilterForm(forms.Form):
#    sample = forms.ModelChoiceField(queryset=Sample.objects.all())
#    min_copy = forms.IntegerField(required=False)
#    norm_factor = forms.IntegerField(required=False)
#
#    def __init__(self, *args, **kwargs):
#        if 'initial' in kwargs:
#            if 'sample_id' in kwargs['initial']:
#                kwargs['initial']['sample'] = kwargs['initial']['sample_id']
#                del kwargs['initial']['sample_id']
#                del kwargs['initial']['id']
#        forms.Form.__init__(self, *args, **kwargs)


class ClonoFilterForm(forms.ModelForm):
    class Meta:
        model = ClonoFilter

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            if 'sample_id' in kwargs['initial']:
                kwargs['initial']['sample'] = kwargs['initial']['sample_id']
                del kwargs['initial']['sample_id']
                del kwargs['initial']['id']
        forms.ModelForm.__init__(self, *args, **kwargs)

        for key in self.fields:
            if not key is 'sample':
                self.fields[key].required = False
