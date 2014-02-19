from django.db import models
from samples.models import Sample
from clonotypes.models import AminoAcid, ClonoFilter
from cf_copmarisons.models import Comparison
import json

class ComparisonToSharedAmino(models.Model):
    '''
    Table that stores shared amino acid keys as a json blob.
    By default, sorts the the input according to variance of
    observed frequencies in all clonofilters
    '''
    comparison = models.ForeignKey(Comparison, unique=True)
    _amino_acids = models.TextField(null=True, db_column='amino_acids')
    def get_amino_acids(self):
        jsonDec = json.decoder.JSONDecoder()
        try:
            return jsonDec.decode(self._amino_acids)
        except:
            return []

    def update_amino_acids(self):
        from numpy import std
        cfs = comparison.clonofilters_all()

        if len(cfs) > 1:
            cf2a_tuples = [ClonoFilterToAmino.objects.get_or_create(clonofilter=cf) for cf in cfs]
            amino_acids = [cf2a.amino_acids for cf2a, created in cf2a_tuples]
            shared_amino_acids_pks = set.intersection(*map(set, amino_acids))

            freq_std = []
            for amino_acid in shared_amino_acids:
                amino_acid_freqs = []
                for recombination in amino_acid.recombination_set.all():
                    for clonotype in recombination.clonotype_set.all():
                        if clonotype.sample in samples:
                            for cfid in sampleid2cfid[clonotype.sample.id]:
                                amino_acid_freqs.append(1.0*clonotype.count/cfid2cf[cfid].size())
                freq_std.append(std(amino_acid_freqs))

            *sorted(zip(freq_std, shared_amino_acid_pks))

            self._amino_acids = json.dumps(shared_amino_acids_pk)
            self.save()
        else:
            raise Exception("Comparison used in ComparisonToSharedAmino object has 1 or less clonofilters");

    amino_acids = property(get_amino_acids)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(ComparisonToSharedAmino, self).save(*args, **kwargs)
            self.update_amino_acids()
        else:
            super(ComparisonToSharedAmino, self).save(*args, **kwargs)


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

class ClonoFilterToAmino(models.Model):
    '''
    Table that stores a clonofilter and blob containing a python list
    of amino acid primary keys
    '''
    clonofilter = models.ForeignKey(ClonoFilter, unique=True)
    _amino_acids = models.TextField(null=True, db_column='amino_acids')

    def get_amino_acids(self):
        jsonDec = json.decoder.JSONDecoder()
        try:
            return jsonDec.decode(self._amino_acids)
        except:
            return []

    def update_amino_acids(self):
        amino_acid_keys = [aa.id for aa in AminoAcid.objects.filter(recombination__clonotype__in=self.clonofilter.get_clonotypes())]
        self._amino_acids = json.dumps(amino_acid_keys)
        self.save()

    amino_acids = property(get_amino_acids)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(ClonoFilterToAmino, self).save(*args, **kwargs)
            self.update_amino_acids()
        else:
            super(ClonoFilterToAmino, self).save(*args, **kwargs)

