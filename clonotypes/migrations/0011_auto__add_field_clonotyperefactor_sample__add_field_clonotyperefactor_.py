# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ClonotypeRefactor.sample'
        db.add_column('clonotypes_clonotyperefactor', 'sample',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['samples.Sample']),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.sequence_id'
        db.add_column('clonotypes_clonotyperefactor', 'sequence_id',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=100),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.container'
        db.add_column('clonotypes_clonotyperefactor', 'container',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=100),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.normalized_frequency'
        db.add_column('clonotypes_clonotyperefactor', 'normalized_frequency',
                      self.gf('django.db.models.fields.FloatField')(default=0.1),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.normalized_copy'
        db.add_column('clonotypes_clonotyperefactor', 'normalized_copy',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.raw_frequency'
        db.add_column('clonotypes_clonotyperefactor', 'raw_frequency',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'ClonotypeRefactor.copy'
        db.add_column('clonotypes_clonotyperefactor', 'copy',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClonotypeRefactor.sample'
        db.delete_column('clonotypes_clonotyperefactor', 'sample_id')

        # Deleting field 'ClonotypeRefactor.sequence_id'
        db.delete_column('clonotypes_clonotyperefactor', 'sequence_id')

        # Deleting field 'ClonotypeRefactor.container'
        db.delete_column('clonotypes_clonotyperefactor', 'container')

        # Deleting field 'ClonotypeRefactor.normalized_frequency'
        db.delete_column('clonotypes_clonotyperefactor', 'normalized_frequency')

        # Deleting field 'ClonotypeRefactor.normalized_copy'
        db.delete_column('clonotypes_clonotyperefactor', 'normalized_copy')

        # Deleting field 'ClonotypeRefactor.raw_frequency'
        db.delete_column('clonotypes_clonotyperefactor', 'raw_frequency')

        # Deleting field 'ClonotypeRefactor.copy'
        db.delete_column('clonotypes_clonotyperefactor', 'copy')


    models = {
        'clonotypes.aminoacid': {
            'Meta': {'object_name': 'AminoAcid'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True'}),
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
        'clonotypes.clonotyperefactor': {
            'Meta': {'object_name': 'ClonotypeRefactor'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalized_copy': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_frequency': ('django.db.models.fields.FloatField', [], {}),
            'raw_frequency': ('django.db.models.fields.FloatField', [], {}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samples.Sample']"}),
            'sequence_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'clonotypes.rearrangement': {
            'Meta': {'object_name': 'Rearrangement'},
            'amino_acid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clonotypes.AminoAcid']", 'null': 'True', 'blank': 'True'}),
            'cdr3_length': ('django.db.models.fields.IntegerField', [], {}),
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
            'nucleotide': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
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
