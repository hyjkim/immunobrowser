from django.core.management.base import BaseCommand, CommandError
from clonotypes.models import Clonotype
#from clonotypes.models import ClonotypeRefactor
from samples.models import Sample


class Command(BaseCommand):
  args = '<sample_id tsv_filename>'
  help = 'Imports a TSV file for a predefined patient'

  def handle(self, *args, **options):
    try:
      sample_id, tsv_filename = args
#    self.stdout.write(" ".join(args))
      self.stdout.write( sample_id + " " + tsv_filename)
    except:
      raise BaseException("Incorrect number of arguments for import")

    try:
      sample = Sample.objects.get(id=sample_id)
    except:
      raise BaseException("Sample with sample id " + sample_id + " not found.")

    Clonotype.import_tsv(sample, tsv_filename)
#    ClonotypeRefactor.import_tsv(sample, tsv_filename)
