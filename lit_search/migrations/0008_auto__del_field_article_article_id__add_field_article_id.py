# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.article_id'
        db.delete_column(u'lit_search_article', 'article_id')

        # Adding field 'Article.id'
        db.add_column(u'lit_search_article', 'id',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Article.article_id'
        db.add_column(u'lit_search_article', 'article_id',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'Article.id'
        db.delete_column(u'lit_search_article', 'id')


    models = {
        u'lit_search.article': {
            'Meta': {'object_name': 'Article'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'article_section': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'article_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'author_affiliations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'author_emails': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'e_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fulltext_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'journal': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'journal_unique_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'orig_file': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'page': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pmc_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'vol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'lit_search.blatquery': {
            'Meta': {'object_name': 'BlatQuery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'})
        }
    }

    complete_apps = ['lit_search']