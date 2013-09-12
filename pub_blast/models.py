from django.db import models
from celery.result import AsyncResult
from pub_blast.tasks import blast

# Create your models here.
class BlastQuery(models.Model):
    task_id = models.CharField(max_length=36, null=True)


    def ready(self):
        '''
        Checks celery for complete job
        '''
        res = AsyncResult(self.task_id)
        return res.ready()

    def fasta_path(self):
        '''
        Define fasta paths by convention rather than in the db.
        Fasta files for queries are stored in media/pub_blast/
        as '%s.fa'%(self.id)
        '''
        return 'media/pub_blast/%s.fa'%(self.id)

    def result_path(self):
        '''
        Define result paths by convention rather than in the db.
        Fasta files for queries are stored in media/pub_blast/
        as '%s.html'%(self.id)
        '''
        return 'media/pub_blast/%s.html'%(self.id)

    @staticmethod
    def new_query(query):
        '''
        Static method that generates a new blast
        query object from valid fasta input
        '''
        blast_query = BlastQuery()
        blast_query.save()

        # Here launch a celery thread to call the blast job
        task = blast.delay(blast_query, query)
        blast_query.task_id = task.task_id
        blast_query.save()

        return blast_query
