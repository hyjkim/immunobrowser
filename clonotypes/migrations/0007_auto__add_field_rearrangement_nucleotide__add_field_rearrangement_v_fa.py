# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rearrangement.nucleotide'
        db.add_column('clonotypes_rearrangement', 'nucleotide',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=300),
                      keep_default=False)

        # Adding field 'Rearrangement.v_family_name'
        db.add_column('clonotypes_rearrangement', 'v_family_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.v_gene_name'
        db.add_column('clonotypes_rearrangement', 'v_gene_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.v_ties'
        db.add_column('clonotypes_rearrangement', 'v_ties',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.d_gene_name'
        db.add_column('clonotypes_rearrangement', 'd_gene_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.j_gene_name'
        db.add_column('clonotypes_rearrangement', 'j_gene_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.j_ties'
        db.add_column('clonotypes_rearrangement', 'j_ties',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.sequence_status'
        db.add_column('clonotypes_rearrangement', 'sequence_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Rearrangement.v_deletion'
        db.add_column('clonotypes_rearrangement', 'v_deletion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.d5_deletion'
        db.add_column('clonotypes_rearrangement', 'd5_deletion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.d3_deletion'
        db.add_column('clonotypes_rearrangement', 'd3_deletion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.j_deletion'
        db.add_column('clonotypes_rearrangement', 'j_deletion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.n2_insertion'
        db.add_column('clonotypes_rearrangement', 'n2_insertion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.n1_insertion'
        db.add_column('clonotypes_rearrangement', 'n1_insertion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.v_index'
        db.add_column('clonotypes_rearrangement', 'v_index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.n1_index'
        db.add_column('clonotypes_rearrangement', 'n1_index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.n2_index'
        db.add_column('clonotypes_rearrangement', 'n2_index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.d_index'
        db.add_column('clonotypes_rearrangement', 'd_index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rearrangement.j_index'
        db.add_column('clonotypes_rearrangement', 'j_index',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rearrangement.nucleotide'
        db.delete_column('clonotypes_rearrangement', 'nucleotide')

        # Deleting field 'Rearrangement.v_family_name'
        db.delete_column('clonotypes_rearrangement', 'v_family_name')

        # Deleting field 'Rearrangement.v_gene_name'
        db.delete_column('clonotypes_rearrangement', 'v_gene_name')

        # Deleting field 'Rearrangement.v_ties'
        db.delete_column('clonotypes_rearrangement', 'v_ties')

        # Deleting field 'Rearrangement.d_gene_name'
        db.delete_column('clonotypes_rearrangement', 'd_gene_name')

        # Deleting field 'Rearrangement.j_gene_name'
        db.delete_column('clonotypes_rearrangement', 'j_gene_name')

        # Deleting field 'Rearrangement.j_ties'
        db.delete_column('clonotypes_rearrangement', 'j_ties')

        # Deleting field 'Rearrangement.v_deletion'
        db.delete_column('clonotypes_rearrangement', 'v_deletion')

        # Deleting field 'Rearrangement.d5_deletion'
        db.delete_column('clonotypes_rearrangement', 'd5_deletion')

        # Deleting field 'Rearrangement.d3_deletion'
        db.delete_column('clonotypes_rearrangement', 'd3_deletion')

        # Deleting field 'Rearrangement.j_deletion'
        db.delete_column('clonotypes_rearrangement', 'j_deletion')

        # Deleting field 'Rearrangement.n2_insertion'
        db.delete_column('clonotypes_rearrangement', 'n2_insertion')

        # Deleting field 'Rearrangement.n1_insertion'
        db.delete_column('clonotypes_rearrangement', 'n1_insertion')

        # Deleting field 'Rearrangement.sequence_status'
        db.delete_column('clonotypes_rearrangement', 'sequence_status')

        # Deleting field 'Rearrangement.v_index'
        db.delete_column('clonotypes_rearrangement', 'v_index')

        # Deleting field 'Rearrangement.n1_index'
        db.delete_column('clonotypes_rearrangement', 'n1_index')

        # Deleting field 'Rearrangement.n2_index'
        db.delete_column('clonotypes_rearrangement', 'n2_index')

        # Deleting field 'Rearrangement.d_index'
        db.delete_column('clonotypes_rearrangement', 'd_index')

        # Deleting field 'Rearrangement.j_index'
        db.delete_column('clonotypes_rearrangement', 'j_index')


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
        'clonotypes.rearrangement': {
            'Meta': {'object_name': 'Rearrangement'},
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
