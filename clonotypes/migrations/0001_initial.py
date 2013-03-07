# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Clonotype'
        db.create_table('clonotypes_clonotype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samples.Sample'])),
            ('sequence_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nucleotide', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('amino_acid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('normalized_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('normalized_copy', self.gf('django.db.models.fields.IntegerField')()),
            ('raw_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('copy', self.gf('django.db.models.fields.IntegerField')()),
            ('cdr3_length', self.gf('django.db.models.fields.IntegerField')()),
            ('v_family_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('d_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('j_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('j_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('d5_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('d3_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('j_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('n2_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('n1_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('sequence_status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_index', self.gf('django.db.models.fields.IntegerField')()),
            ('n1_index', self.gf('django.db.models.fields.IntegerField')()),
            ('n2_index', self.gf('django.db.models.fields.IntegerField')()),
            ('d_index', self.gf('django.db.models.fields.IntegerField')()),
            ('j_index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('clonotypes', ['Clonotype'])

        # Adding model 'ClonoFilter'
        db.create_table('clonotypes_clonofilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samples.Sample'])),
            ('min_copy', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('clonotypes', ['ClonoFilter'])


    def backwards(self, orm):
        # Deleting model 'Clonotype'
        db.delete_table('clonotypes_clonotype')

        # Deleting model 'ClonoFilter'
        db.delete_table('clonotypes_clonofilter')


    models = {
        'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samples.Sample']"})
        },
        'clonotypes.clonotype': {
            'Meta': {'object_name': 'Clonotype'},
            'amino_acid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cdr3_length': ('django.db.models.fields.IntegerField', [], {}),
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
            'd3_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'd5_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'd_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'd_index': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'j_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'j_index': ('django.db.models.fields.IntegerField', [], {}),
            'j_ties': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'n1_index': ('django.db.models.fields.IntegerField', [], {}),
            'n1_insertion': ('django.db.models.fields.IntegerField', [], {}),
            'n2_index': ('django.db.models.fields.IntegerField', [], {}),
            'n2_insertion': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_copy': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_frequency': ('django.db.models.fields.FloatField', [], {}),
            'nucleotide': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'raw_frequency': ('django.db.models.fields.FloatField', [], {}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samples.Sample']"}),
            'sequence_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sequence_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'v_family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_index': ('django.db.models.fields.IntegerField', [], {}),
            'v_ties': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['clonotypes']