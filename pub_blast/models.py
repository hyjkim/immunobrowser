from django.db import models
from django.core.files import File

# Create your models here.
class BlastQuery(models.Model):
    task_id = models.CharField(max_length=36, null=True)

    @staticmethod
    def new_query(query):
        '''
        Static method that generates a new blast
        query object from valid fasta input
        '''
        blast_query = BlastQuery()
        blast_query.save()

        fasta = open('media/pub_blast/%s.fa' % (blast_query.id), 'w')
        fasta.write(query)
        fasta.close()

        # Here launch a celery thread to call the blast job

        return blast_query
