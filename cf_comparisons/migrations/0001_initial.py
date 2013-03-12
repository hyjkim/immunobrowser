# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comparison'
        db.create_table('cf_comparisons_comparison', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cf_comparisons', ['Comparison'])

        # Adding M2M table for field clonofilters on 'Comparison'
        db.create_table('cf_comparisons_comparison_clonofilters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comparison', models.ForeignKey(orm['cf_comparisons.comparison'], null=False)),
            ('clonofilter', models.ForeignKey(orm['clonotypes.clonofilter'], null=False))
        ))
        db.create_unique('cf_comparisons_comparison_clonofilters', ['comparison_id', 'clonofilter_id'])


    def backwards(self, orm):
        # Deleting model 'Comparison'
        db.delete_table('cf_comparisons_comparison')

        # Removing M2M table for field clonofilters on 'Comparison'
        db.delete_table('cf_comparisons_comparison_clonofilters')


    models = {
        'cf_comparisons.comparison': {
            'Meta': {'object_name': 'Comparison'},
            'clonofilters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clonotypes.ClonoFilter']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samples.Sample']"})
        },
        'patients.patient': {
            'Meta': {'object_name': 'Patient'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'disease': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'samples.sample': {
            'Meta': {'object_name': 'Sample'},
            'cell_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'draw_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Patient']"})
        }
    }

    complete_apps = ['cf_comparisons']