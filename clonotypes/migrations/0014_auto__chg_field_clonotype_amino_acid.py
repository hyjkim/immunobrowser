# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Clonotype.amino_acid' to match new field type.
        db.rename_column(u'clonotypes_clonotype', 'amino_acid', 'amino_acid_id')
        # Changing field 'Clonotype.amino_acid'
        db.alter_column(u'clonotypes_clonotype', 'amino_acid_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.AminoAcid'], null=True))
        # Adding index on 'Clonotype', fields ['amino_acid']
        db.create_index(u'clonotypes_clonotype', ['amino_acid_id'])


    def backwards(self, orm):
        # Removing index on 'Clonotype', fields ['amino_acid']
        db.delete_index(u'clonotypes_clonotype', ['amino_acid_id'])


        # User chose to not deal with backwards NULL issues for 'Clonotype.amino_acid'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.amino_acid' and its values cannot be restored.")

    models = {
        u'clonotypes.aminoacid': {
            'Meta': {'object_name': 'AminoAcid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'samples': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['samples.Sample']", 'symmetrical': 'False'}),
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
            'amino_acid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.AminoAcid']", 'null': 'True', 'blank': 'True'}),
            'cdr3_length': ('django.db.models.fields.IntegerField', [], {}),
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
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
            'normalized_copy': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_frequency': ('django.db.models.fields.FloatField', [], {}),
            'nucleotide': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'raw_frequency': ('django.db.models.fields.FloatField', [], {}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"}),
            'sequence_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sequence_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_deletion': ('django.db.models.fields.IntegerField', [], {}),
            'v_family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_index': ('django.db.models.fields.IntegerField', [], {}),
            'v_ties': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'clonotypes.clonotyperefactor': {
            'Meta': {'object_name': 'ClonotypeRefactor'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalized_copy': ('django.db.models.fields.IntegerField', [], {}),
            'normalized_frequency': ('django.db.models.fields.FloatField', [], {}),
            'raw_frequency': ('django.db.models.fields.FloatField', [], {}),
            'rearrangement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.Rearrangement']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"}),
            'sequence_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'clonotypes.rearrangement': {
            'Meta': {'object_name': 'Rearrangement'},
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