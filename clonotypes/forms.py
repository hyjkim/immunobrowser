from django import forms
from samples.models import Sample


class ClonoFilterForm(forms.Form):
    sample = forms.ModelChoiceField(queryset=Sample.objects.all())
#    sample = forms.ModelChoiceField()
    #sample = forms.IntegerField(widget=forms.TextInput(
    #    attrs={'class': 'disabled', 'readonly': 'readonly'}))
    min_copy = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
#        forms.Form.__init__(self, *args, **kwargs)
        if 'initial' in kwargs:
            if 'sample_id' in kwargs['initial']:
                kwargs['initial']['sample'] = kwargs['initial']['sample_id']
                del kwargs['initial']['sample_id']
                del kwargs['initial']['id']
#                self.sample.initial = Sample.objects.get(kwargs['initial']['sample_id'])
        forms.Form.__init__(self, *args, **kwargs)
