from django import forms
from samples.models import Sample


class SampleCompareForm(forms.Form):
    samples = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(),
                                             widget=forms.SelectMultiple(
                                                 attrs={'size': 12}),
                                             )
