from django.db import models
import gzip
import csv
import time
from utils.text_manipulation import convert
from utils.utils import sub_dict_remove_strict
from celery.result import AsyncResult
from lit_search.tasks import blat

# Create your models here.
class BlatQuery(models.Model):
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
        Fasta files for queries are stored in media/lit_search/
        as '%s.fa'%(self.id)
        '''
        return 'media/lit_search/%s.fa'%(self.id)

    def result_path(self):
        '''
        Define result paths by convention rather than in the db.
        Fasta files for queries are stored in media/lit_search/
        as '%s.html'%(self.id)
        '''
        return 'media/lit_search/%s.psl'%(self.id)

    @staticmethod
    def new_query(query):
        '''
        Static method that generates a new blat
        query object from valid fasta input
        '''
        blat_query = BlatQuery()
        blat_query.save()

        # Here launch a celery thread to call the blat job
        task = blat.delay(blat_query, query)
        blat_query.task_id = task.task_id
        blat_query.save()

        return blat_query

# Create your models here.
class Article(models.Model):
    '''
    Stores a paper from Max's literature mining pipeline
    '''
    article_id = models.BigIntegerField()
    external_id = models.CharField(max_length=255)
    source = models.CharField(null=True, max_length=255)
    orig_file = models.CharField(null=True, max_length=30)
    journal = models.TextField(null=True)
    print_issn = models.CharField(null=True, max_length=9)
    e_issn = models.CharField(null=True, max_length=9)
    journal_unique_id = models.CharField(null=True, max_length=30)
    year = models.IntegerField(null=True)
    article_type = models.CharField(null=True, max_length=255)
    article_section = models.CharField(null=True, max_length=255)
    authors = models.TextField(null=True)
    author_emails = models.TextField(null=True)
    author_affiliations = models.TextField(null=True)
    keywords = models.TextField(null=True)
    title = models.TextField(null=True)
    abstract = models.TextField(null=True)
    vol = models.CharField(null=True, max_length=30)
    issue = models.CharField(null=True, max_length=30)
    page = models.IntegerField(null=True)
    pmid = models.IntegerField(null=True)
    pmc_id = models.IntegerField(null=True)
    doi = models.CharField(null=True, max_length=255)
    fulltext_url = models.URLField(null=True)
    time = models.DateTimeField(null=True)

    @staticmethod
    def import_articles(filename):
        '''
        Used to import a file directly into the database
        '''
        num_to_insert = 500
        article_list = []
        article_cols = [
            'article_id',
            'external_id',
            'source',
            'orig_file',
            'journal',
            'print_issn',
            'e_issn',
            'journal_unique_id',
            'year',
            'article_type',
            'article_section',
            'authors',
            'author_emails',
            'author_affiliations',
            'keywords',
            'title',
            'abstract',
            'vol',
            'issue',
            'page',
            'pmid',
            'pmc_id',
            'doi',
            'fulltext_url',
            'time',
        ]

        with gzip.open(filename) as f:
            reader = csv.reader(f, delimiter="\t")
            count = 0

            for row in reader:
                if reader.line_num == 1:
                    headers = row
                    headers = map(convert, headers)
                    if (headers[0] == '#article_id'):
                        headers[0] = 'article_id'
                elif len(article_list) >= num_to_insert:
                    Article.objects.bulk_create(article_list)
                    print "bulk updating %s articles" % (len(article_list))
                    article_list = []
                else:
                    line_dict = {}
                    line_dict = dict(zip(headers, row))
                    article_dict = sub_dict_remove_strict(
                        line_dict, article_cols)
                    if line_dict:
                        raise Exception('Unidentified column in file')
                    # convert int columns from string to int
                    ints  = ['article_id', 'year', 'page', 'pmid', 'pmc_id']
                    for field in ints:
                        if (article_dict[field] == ''):
                            article_dict[field] = None
                        else:
                            article_dict[field] = int(article_dict[field])

                    # convert timestamp to time object
                    try:
                        if (article_dict['time'] == ''):
                            article_dict['time'] = None
                        else:
                            article_dict['time'] = time.strftime("%Y-%m-%d %T",time.strptime(article_dict['time']))
                    except Exception as e:
                        print article_dict['time']
                    # append article to list to be bulk created
                    count += 1
                    article_list.append(Article(**article_dict))

            Article.objects.bulk_create(article_list)
