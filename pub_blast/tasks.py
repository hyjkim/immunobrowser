from celery import task
import os

@task()
def blast(blast_query, query):
    '''
    Writes a query to a file and submits it to a blast job
    '''
    # Write the fasta file
    fasta = open('media/pub_blast/%s.fa' % (blast_query.id), 'w')
    fasta.write(query)
    fasta.close()
    # Call external script
    os.system('python external/blast_placeholder.py %s %s' % (blast_query.fasta_path(), blast_query.result_path()))
