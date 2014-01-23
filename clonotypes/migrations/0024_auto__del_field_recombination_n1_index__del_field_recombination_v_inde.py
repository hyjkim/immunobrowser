# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Recombination.n1_index'
        db.delete_column(u'clonotypes_recombination', 'n1_index')

        # Deleting field 'Recombination.v_index'
        db.delete_column(u'clonotypes_recombination', 'v_index')

        # Deleting field 'Recombination.n1_insertion'
        db.delete_column(u'clonotypes_recombination', 'n1_insertion')

        # Deleting field 'Recombination.d_index'
        db.delete_column(u'clonotypes_recombination', 'd_index')

        # Deleting field 'Recombination.v_family_name'
        db.delete_column(u'clonotypes_recombination', 'v_family_name')

        # Deleting field 'Recombination.n2_index'
        db.delete_column(u'clonotypes_recombination', 'n2_index')

        # Deleting field 'Recombination.j_index'
        db.delete_column(u'clonotypes_recombination', 'j_index')

        # Deleting field 'Recombination.n2_insertion'
        db.delete_column(u'clonotypes_recombination', 'n2_insertion')

        # Deleting field 'Clonotype.sequence_id'
        db.delete_column(u'clonotypes_clonotype', 'sequence_id')

        # Deleting field 'Clonotype.copy'
        db.delete_column(u'clonotypes_clonotype', 'copy')

        # Deleting field 'Clonotype.raw_frequency'
        db.delete_column(u'clonotypes_clonotype', 'raw_frequency')

        # Deleting field 'Clonotype.container'
        db.delete_column(u'clonotypes_clonotype', 'container')

        # Deleting field 'Clonotype.normalized_copy'
        db.delete_column(u'clonotypes_clonotype', 'normalized_copy')

        # Deleting field 'Clonotype.normalized_frequency'
        db.delete_column(u'clonotypes_clonotype', 'normalized_frequency')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Recombination.n1_index'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.n1_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.v_index'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.v_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.n1_insertion'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.n1_insertion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.d_index'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.d_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.v_family_name'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.v_family_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.n2_index'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.n2_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.j_index'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.j_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Recombination.n2_insertion'
        raise RuntimeError("Cannot reverse this migration. 'Recombination.n2_insertion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.sequence_id'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.sequence_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.copy'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.copy' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.raw_frequency'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.raw_frequency' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.container'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.container' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.normalized_copy'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.normalized_copy' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.normalized_frequency'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.normalized_frequency' and its values cannot be restored.")

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
        u'clonotypes.aminoacid': {
            'Meta': {'object_name': 'AminoAcid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'clonotypes.clonofilter': {
            'Meta': {'object_name': 'ClonoFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'max_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_copy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'min_length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'norm_factor': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"}),
            'v_family_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'clonotypes.clonofilter2': {
            'Meta': {'object_name': 'ClonoFilter2'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"})
        },
        u'clonotypes.clonotype': {
            'Meta': {'object_name': 'Clonotype'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'frequency': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recombination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.Recombination']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"})
        },
        u'clonotypes.recombination': {
            'Meta': {'object_name': 'Recombination'},
            'amino_acid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clonotypes.AminoAcid']", 'null': 'True', 'blank': 'True'}),
            'cdr3_length': ('django.db.models.fields.IntegerField', [], {}),
            'd3_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'd5_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'd_end': ('django.db.models.fields.IntegerField', [], {}),
            'd_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'd_start': ('django.db.models.fields.IntegerField', [], {}),
            'd_ties': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dj_insertion': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'j_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'j_start': ('django.db.models.fields.IntegerField', [], {}),
            'j_ties': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nucleotide': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sequence_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'v_end': ('django.db.models.fields.IntegerField', [], {}),
            'v_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_ties': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'vd_insertion': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['clonotypes']