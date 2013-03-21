# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Rearrangement'
        db.delete_table(u'clonotypes_rearrangement')

        # Adding model 'Recombination'
        db.create_table(u'clonotypes_recombination', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nucleotide', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('v_family_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('d_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('j_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('j_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sequence_status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('d5_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('d3_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('j_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('n2_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('n1_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('v_index', self.gf('django.db.models.fields.IntegerField')()),
            ('n1_index', self.gf('django.db.models.fields.IntegerField')()),
            ('n2_index', self.gf('django.db.models.fields.IntegerField')()),
            ('d_index', self.gf('django.db.models.fields.IntegerField')()),
            ('j_index', self.gf('django.db.models.fields.IntegerField')()),
            ('cdr3_length', self.gf('django.db.models.fields.IntegerField')()),
            ('amino_acid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.AminoAcid'], null=True, blank=True)),
        ))
        db.send_create_signal(u'clonotypes', ['Recombination'])

        # Deleting field 'Clonotype.rearrangement'
        db.delete_column(u'clonotypes_clonotype', 'rearrangement_id')

        # Adding field 'Clonotype.recombination'
        db.add_column(u'clonotypes_clonotype', 'recombination',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['clonotypes.Recombination']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Rearrangement'
        db.create_table(u'clonotypes_rearrangement', (
            ('d5_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('j_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('j_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('amino_acid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.AminoAcid'], null=True, blank=True)),
            ('n1_index', self.gf('django.db.models.fields.IntegerField')()),
            ('d_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_index', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cdr3_length', self.gf('django.db.models.fields.IntegerField')()),
            ('j_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('v_ties', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('n1_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('d_index', self.gf('django.db.models.fields.IntegerField')()),
            ('sequence_status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('n2_index', self.gf('django.db.models.fields.IntegerField')()),
            ('j_index', self.gf('django.db.models.fields.IntegerField')()),
            ('n2_insertion', self.gf('django.db.models.fields.IntegerField')()),
            ('d3_deletion', self.gf('django.db.models.fields.IntegerField')()),
            ('nucleotide', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('v_family_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_gene_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('v_deletion', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'clonotypes', ['Rearrangement'])

        # Deleting model 'Recombination'
        db.delete_table(u'clonotypes_recombination')


        # User chose to not deal with backwards NULL issues for 'Clonotype.rearrangement'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.rearrangement' and its values cannot be restored.")
        # Deleting field 'Clonotype.recombination'
        db.delete_column(u'clonotypes_clonotype', 'recombination_id')


    models = {
        u'clonotypes.aminoacid': {
            'Meta': {'object_name': 'AminoAcid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"})
        },
        u'clonotypes.clonotype': {
            'Meta': {'object_name': 'Clonotype'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalized_copy': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_frequency': ('django.db.models.fields.FloatField', [], {}),
            'raw_frequency': ('django.db.models.fields.FloatField', [], {}),
            'recombination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.Recombination']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"}),
            'sequence_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'clonotypes.recombination': {
            'Meta': {'object_name': 'Recombination'},
            'amino_acid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.AminoAcid']", 'null': 'True', 'blank': 'True'}),
            'cdr3_length': ('django.db.models.fields.IntegerField', [], {}),
            'd3_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'd5_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'd_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'd_index': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

    complete_apps = ['clonotypes']