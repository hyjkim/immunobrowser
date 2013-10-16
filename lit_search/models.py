from django.db import models
import os
import gzip
import csv
import time
from utils.text_manipulation import convert
from utils.utils import sub_dict_remove_strict
from celery.result import AsyncResult
from lit_search.tasks import blat
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


class BlatHitException(Exception):
    pass

def prot_seq(sequence):
    # strip non base characters

#    sequence = sequence.translate(None, '[^acgtACGT]')
    print sequence
    overflow = len(sequence) % 3
    sequence = sequence[:-overflow]
    return Seq(sequence, generic_dna).translate()

def colorize(sequence):
    '''
    Given a protein sequence, wrap each amino acid
    in a span that colorizes it
    '''
    COLORS = {
        'W': 'blue',
        'L': 'blue',
        'V': 'blue',
        'I': 'blue',
        'M': 'blue',
        'F': 'blue',
        'A': 'blue',
        'C': 'blue',
        'K': 'red',
        'R': 'red',
        'T': 'green',
        'S': 'green',
        'N': 'green',
        'Q': 'green',
        'C': 'pink',
        'D': 'magenta',
        'E': 'magenta',
        'G': 'orange',
        'H': 'cyan',
        'Y': 'cyan',
        'P': 'yellow',
    }
    color_seq = ''
    for aa in sequence:
        if aa in COLORS:
            color_seq += '<span class="aa-%s">%s</span>' % (COLORS[aa], aa)
        else:
            color_seq += aa
    return color_seq


class BlatHit():
    '''
    BlatHist contains all the fields of a pslx file (output from blat)
    '''
    article = None
    fields = ['match', 'mismatch', 'rep_match', 'n', 'q_gap_count',
              'q_gap_bases', 't_gap_count', 't_gap_bases', 'strand',
              'q_name', 'q_size', 'q_start', 'q_end', 't_name', 't_size', 't_start',
              't_end', 'block_count', 'block_sizes', 'q_starts', 't_starts',
              'q_seq', 't_seq']

    def __init__(self, *args):
        if len(args) > 1:
            raise BlatHitException('Expected single argument to init BlatHit')
        result_string = args[0]
        if not (isinstance(result_string, str)):
            raise BlatHitException('Expected String, found %s' % (type(result_string)))
        result_list = result_string.split('\t')
        if not (len(result_list) == len(self.fields)):
            raise BlatHitException('Expected %s fields, found %s' %(len(self.fields), len(result_list)))
        for key, value in dict(zip(self.fields, result_list)).iteritems():
            setattr(self, key, value)


    def q_prot(self):
        sequences = self.q_seq.split(',')
        return prot_seq(sequences[0])

    def t_prot(self):
        sequences = self.t_seq.split(',')
        return prot_seq(sequences[0])

    def t_color(self):
        '''
        outputs colorized version of t_seq
        '''
        return colorize(self.t_seq)

    def q_color(self):
        '''
        outputs colorized version of q_seq
        '''
        return colorize(self.q_seq)

    def html_alignment(self):
        '''
        Outputs an alignment of target vs query and colorizes amino
        acids based on clustal/pfam colors obtained from
        http://ekhidna.biocenter.helsinki.fi/pfam2/clustal_colours
        '''
        return colorize(self.t_seq) + '<br />' + colorize(self.q_seq)


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
        return 'media/lit_search/%s.fa' % (self.id)

    def result_path(self):
        '''
        Define result paths by convention rather than in the db.
        Fasta files for queries are stored in media/lit_search/
        as '%s.html'%(self.id)
        '''
        return 'media/lit_search/%s.pslx' % (self.id)

    def hits_safe(self):
        '''
        Returns a list of BlatHit objects and assigns the article field.
        Hits the database once for each article, but can handle cases
        where the article does not exist in the database
        '''
        blathits = []
        # open result file
        result_file = open(self.result_path(), 'r')
        # skip first 5 lines (header lines)
        for _ in xrange(5):
            next(result_file)
        # create a new hit file for each line
        for line in result_file:
            hit = BlatHit(line)
            blathits.append(hit)
            try:
                hit.article = Article.objects.get(id=hit.t_name[:9])
            except:
                pass
        # return list of BlatHit
        return blathits

    def hits_by_article(self):
        '''
        Returns a dict of BlatHit objects where an article is the key
        '''
        from collections import defaultdict
        from utils.utils import undefaulted

        hit_dict = defaultdict(list)
        hits = self.hits();
        for hit in hits:
            hit_dict[hit.article].append(hit);
        return undefaulted(hit_dict)

    def hits(self):
        '''
        Returns a list of BlatHit objects and assigns the article field.
        Tries to use an in_bulk query in order to minimize database hits
        but this only works if sequences in fasta files are guaranteed
        to be in the database
        '''
        blathits = []
        # open result file
        result_file = open(self.result_path(), 'r')
        # skip first 5 lines (header lines)
        for _ in xrange(5):
            next(result_file)
        # create a new hit file for each line
        for line in result_file:
            blathits.append(BlatHit(line))
        # Get article objects
        article_ids = [hit.t_name[:10] for hit in blathits]
        articles = Article.objects.in_bulk(article_ids)
        # add articles id with Article models
        for hit in blathits:
            hit.article = articles[hit.t_name[:10]]
        # return list of BlatHit
        return blathits

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

class Article(models.Model):
    '''
    Stores a paper from Max's literature mining pipeline
    '''
    id = models.CharField(max_length=12, primary_key=True)
    external_id = models.CharField(max_length=255)
    source = models.CharField(null=True, max_length=255)
    orig_file = models.CharField(null=True, max_length=30)
    journal = models.TextField(null=True)
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
            'id',
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
                        headers[0] = 'id'
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
                    ints = ['year', 'page', 'pmid', 'pmc_id']
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
                            article_dict['time'] = time.strftime("%Y-%m-%d %T", time.strptime(article_dict['time']))
                    except Exception as e:
                        print e
                        print article_dict['time']
                    # append article to list to be bulk created
                    count += 1
                    article_list.append(Article(**article_dict))

            Article.objects.bulk_create(article_list)
