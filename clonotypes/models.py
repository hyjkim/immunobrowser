from django.db import models
from samples.models import Sample
from utils.text_manipulation import convert
import csv

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
  d5_deletion = models.IntegerField()
  d3_deletion = models.IntegerField()
  j_deletion = models.IntegerField()
  n2_insertion = models.IntegerField()
  n1_insertion = models.IntegerField()
  sequence_status = models.CharField(max_length=100)
  v_index = models.IntegerField()
  n1_index = models.IntegerField()
  n2_index = models.IntegerField()
  d_index = models.IntegerField()
  j_index = models.IntegerField()

  @staticmethod
  def import_tsv(sample, filename):
    headers = None
    clonotype_list = []
    reader = csv.reader(open(filename, 'r'), delimiter="\t")

    for row in reader:
      if reader.line_num == 1:
        headers = row
        headers = map(convert, headers)
      else:
        clonotype = {}
        clonotype = dict(zip(headers, row))
#        print clonotype
        if(clonotype['normalized_frequency'] == ''):
          raise Exception('Normalized_frequency cannot be null')
        clonotype_list.append(Clonotype(sample=sample, **clonotype))

        #content[row[0]] = dict(zip(headers, row[1:]))
    Clonotype.objects.bulk_create(clonotype_list)






