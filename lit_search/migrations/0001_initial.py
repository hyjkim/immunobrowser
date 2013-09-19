# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'lit_search_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_id', self.gf('django.db.models.fields.IntegerField')()),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('orig_file', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('print_issn', self.gf('django.db.models.fields.CharField')(max_length=9, null=True)),
            ('e_issn', self.gf('django.db.models.fields.CharField')(max_length=9, null=True)),
            ('journal_unique_id', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('article_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('article_section', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('authors', self.gf('django.db.models.fields.TextField')(null=True)),
            ('author_emails', self.gf('django.db.models.fields.TextField')(null=True)),
            ('author_affiliations', self.gf('django.db.models.fields.TextField')(null=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(null=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True)),
            ('vol', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('page', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pmid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pmcid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('fulltext_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'lit_search', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'lit_search_article')


    models = {
        u'lit_search.article': {
            'Meta': {'object_name': 'Article'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'article_id': ('django.db.models.fields.IntegerField', [], {}),
            'article_section': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'article_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'author_affiliations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'author_emails': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'e_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'fulltext_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'journal_unique_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'orig_file': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'page': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pmcid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'vol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['lit_search']