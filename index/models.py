from django.db import models
from samples.models import Sample
from clonotypes.models import AminoAcid
import json

class SampleToAmino(models.Model):
    '''
    Table that stores a sample and blob containing a python list
    of amino acid primary keys
    '''
    sample = models.ForeignKey(Sample, unique=True)
    _amino_acids = models.TextField(null=True, db_column='amino_acids')

    def get_amino_acids(self):
        jsonDec = json.decoder.JSONDecoder()
        try:
            return jsonDec.decode(self._amino_acids)
        except:
            return []

    def update_amino_acids(self):
        amino_acid_keys = [aa.id for aa in AminoAcid.objects.filter(recombination__clonotype__sample=self.sample)]
        self._amino_acids = json.dumps(amino_acid_keys)
        self.save()

    amino_acids = property(get_amino_acids)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(SampleToAmino, self).save(*args, **kwargs)
            self.update_amino_acids()
        else:
            super(SampleToAmino, self).save(*args, **kwargs)

#    def __init__(self, *args, **kwargs):
#        super(SampleToAmino, self).__init__(*args, **kwargs)
#        self.update_amino_acids()
#        print "Creating S2a for %s" %(self.sample)
