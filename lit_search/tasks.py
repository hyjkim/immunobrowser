from celery import task
import os


@task()
def blat(blat_query, query):
    '''
    Writes a query to a file and submits it to a blat job
    '''
    # Write the fasta file
    fasta = open(blat_query.fasta_path(), 'w')
    fasta.write(query)
    fasta.close()
    # Call external script
    os.system('external/litSearch/gfClient -t=dnax -q=prot -out=pslx -minScore=0 localhost 8001 external/litSearch %s %s' % (blat_query.fasta_path(), blat_query.result_path()))
