from django.db import models
from samples.models import Sample

# Create your models here.
class Clonotype(models.Model):
  sample = models.ForeignKey(Sample)
  sequence_id = models.CharField(max_length=100)
  container = models.CharField(max_length=100)
  nucleotide = models.CharField(max_length=300)
  amino_acid = models.CharField(max_length=100)
  normalized_frequency = models.FloatField()
  normalized_copy = models.IntegerField()
  raw_frequency = models.FloatField()
  copy = models.IntegerField()
  cdr3_length = models.IntegerField()
  v_family_name = models.CharField(max_length=100)
  v_gene_name = models.CharField(max_length=100)
  v_ties = models.CharField(max_length=100)
  d_gene_name = models.CharField(max_length=100)
  j_gene_name = models.CharField(max_length=100)
  j_ties = models.CharField(max_length=100)
  v_deletion = models.IntegerField()
  d_5_deletion = models.IntegerField()
  d_3_deletion = models.IntegerField()
  j_deletion = models.IntegerField()
  n_2_insertion = models.IntegerField()
  n_1_insertion = models.IntegerField()
  sequence_status = models.CharField(max_length=100)
  v_index = models.IntegerField()
  n_1_index = models.IntegerField()
  n_2_index = models.IntegerField()
  d_index = models.IntegerField()
  j_index = models.IntegerField()



