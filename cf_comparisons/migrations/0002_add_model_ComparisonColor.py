# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ComparisonColor'
        db.create_table(u'cf_comparisons_comparisoncolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comparison', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cf_comparisons.Comparison'])),
            ('clonofilter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.ClonoFilter'])),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal(u'cf_comparisons', ['ComparisonColor'])


    def backwards(self, orm):
        # Deleting model 'ComparisonColor'
        db.delete_table(u'cf_comparisons_comparisoncolor')


    models = {
        u'cf_comparisons.comparison': {
            'Meta': {'object_name': 'Comparison'},
            'clonofilters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['clonotypes.ClonoFilter']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cf_comparisons.comparisoncolor': {
            'Meta': {'unique_together': "(('comparison', 'clonofilter'),)", 'object_name': 'ComparisonColor'},
            'clonofilter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.ClonoFilter']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'comparison': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cf_comparisons.Comparison']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"})
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
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.Patient']"})
        }
    }

    complete_apps = ['cf_comparisons']