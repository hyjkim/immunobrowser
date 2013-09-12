from django import forms
from django.forms import ValidationError
from Bio import SeqIO
from StringIO import StringIO

class BlastForm(forms.Form):
    query=forms.CharField(widget=forms.Textarea,
            error_messages={'fasta':'Query not valid FASTA format'},
            )

    def clean_query(self):
        '''
        Checks to make sure query is valid fasta sequence with at least one
        fasta sequence
        '''
        try:
            fasta = SeqIO.read(StringIO(self.cleaned_data['query']), 'fasta')
        except:
            raise ValidationError(self.fields['query'].error_messages['fasta'])
        return self.cleaned_data['query']
