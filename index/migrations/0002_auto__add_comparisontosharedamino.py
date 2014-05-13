# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ComparisonToSharedAmino'
        db.create_table(u'index_comparisontosharedamino', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comparison', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cf_comparisons.Comparison'], unique=True)),
            ('_amino_acids', self.gf('django.db.models.fields.TextField')(null=True, db_column='amino_acids')),
        ))
        db.send_create_signal(u'index', ['ComparisonToSharedAmino'])


    def backwards(self, orm):
        # Deleting model 'ComparisonToSharedAmino'
        db.delete_table(u'index_comparisontosharedamino')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cf_comparisons.comparison': {
            'Meta': {'object_name': 'Comparison'},
            '_clonofilters': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'clonofilters_list'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'max_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"}),
            'v_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'index.clonofiltertoamino': {
            'Meta': {'object_name': 'ClonoFilterToAmino'},
            '_amino_acids': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'amino_acids'"}),
            'clonofilter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.ClonoFilter']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'index.comparisontosharedamino': {
            'Meta': {'object_name': 'ComparisonToSharedAmino'},
            '_amino_acids': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'amino_acids'"}),
            'comparison': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cf_comparisons.Comparison']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'index.sampletoamino': {
            'Meta': {'object_name': 'SampleToAmino'},
            '_amino_acids': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'amino_acids'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']", 'unique': 'True'})
        },
        u'patients.patient': {
            'Meta': {'object_name': 'Patient'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'disease': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'samples.sample': {
            'Meta': {'object_name': 'Sample'},
            'cell_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'draw_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.Patient']"}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['index']