# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Recombination.d_ties'
        db.add_column(u'clonotypes_recombination', 'd_ties',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Recombination.vd_insertion'
        db.add_column(u'clonotypes_recombination', 'vd_insertion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Recombination.dj_insertion'
        db.add_column(u'clonotypes_recombination', 'dj_insertion',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Recombination.v_end'
        db.add_column(u'clonotypes_recombination', 'v_end',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Recombination.d_start'
        db.add_column(u'clonotypes_recombination', 'd_start',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Recombination.d_end'
        db.add_column(u'clonotypes_recombination', 'd_end',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Recombination.j_start'
        db.add_column(u'clonotypes_recombination', 'j_start',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Recombination.d5_deletion'
        db.alter_column(u'clonotypes_recombination', 'd5_deletion', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Recombination.j_ties'
        db.alter_column(u'clonotypes_recombination', 'j_ties', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Recombination.j_deletion'
        db.alter_column(u'clonotypes_recombination', 'j_deletion', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Recombination.v_ties'
        db.alter_column(u'clonotypes_recombination', 'v_ties', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

        # Changing field 'Recombination.d3_deletion'
        db.alter_column(u'clonotypes_recombination', 'd3_deletion', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Recombination.v_deletion'
        db.alter_column(u'clonotypes_recombination', 'v_deletion', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Adding field 'Clonotype.frequency'
        db.add_column(u'clonotypes_clonotype', 'frequency',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Clonotype.count'
        db.add_column(u'clonotypes_clonotype', 'count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Recombination.d_ties'
        db.delete_column(u'clonotypes_recombination', 'd_ties')

        # Deleting field 'Recombination.vd_insertion'
        db.delete_column(u'clonotypes_recombination', 'vd_insertion')

        # Deleting field 'Recombination.dj_insertion'
        db.delete_column(u'clonotypes_recombination', 'dj_insertion')

        # Deleting field 'Recombination.v_end'
        db.delete_column(u'clonotypes_recombination', 'v_end')

        # Deleting field 'Recombination.d_start'
        db.delete_column(u'clonotypes_recombination', 'd_start')

        # Deleting field 'Recombination.d_end'
        db.delete_column(u'clonotypes_recombination', 'd_end')

        # Deleting field 'Recombination.j_start'
        db.delete_column(u'clonotypes_recombination', 'j_start')


        # Changing field 'Recombination.d5_deletion'
        db.alter_column(u'clonotypes_recombination', 'd5_deletion', self.gf('django.db.models.fields.IntegerField')(default=1))

        # Changing field 'Recombination.j_ties'
        db.alter_column(u'clonotypes_recombination', 'j_ties', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Recombination.j_deletion'
        db.alter_column(u'clonotypes_recombination', 'j_deletion', self.gf('django.db.models.fields.IntegerField')(default=''))

        # Changing field 'Recombination.v_ties'
        db.alter_column(u'clonotypes_recombination', 'v_ties', self.gf('django.db.models.fields.CharField')(default=-1, max_length=500))

        # Changing field 'Recombination.d3_deletion'
        db.alter_column(u'clonotypes_recombination', 'd3_deletion', self.gf('django.db.models.fields.IntegerField')(default=-1))

        # Changing field 'Recombination.v_deletion'
        db.alter_column(u'clonotypes_recombination', 'v_deletion', self.gf('django.db.models.fields.IntegerField')(default=-1))
        # Deleting field 'Clonotype.frequency'
        db.delete_column(u'clonotypes_clonotype', 'frequency')

        # Deleting field 'Clonotype.count'
        db.delete_column(u'clonotypes_clonotype', 'count')


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
            'container': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copy': ('django.db.models.fields.IntegerField', [], {}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'frequency': ('django.db.models.fields.FloatField', [], {}),
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
            'd3_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'd5_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'd_end': ('django.db.models.fields.IntegerField', [], {}),
            'd_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'd_index': ('django.db.models.fields.IntegerField', [], {}),
            'd_start': ('django.db.models.fields.IntegerField', [], {}),
            'd_ties': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dj_insertion': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'j_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'j_index': ('django.db.models.fields.IntegerField', [], {}),
            'j_start': ('django.db.models.fields.IntegerField', [], {}),
            'j_ties': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'n1_index': ('django.db.models.fields.IntegerField', [], {}),
            'n1_insertion': ('django.db.models.fields.IntegerField', [], {}),
            'n2_index': ('django.db.models.fields.IntegerField', [], {}),
            'n2_insertion': ('django.db.models.fields.IntegerField', [], {}),
            'nucleotide': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sequence_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_deletion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'v_end': ('django.db.models.fields.IntegerField', [], {}),
            'v_family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'v_index': ('django.db.models.fields.IntegerField', [], {}),
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