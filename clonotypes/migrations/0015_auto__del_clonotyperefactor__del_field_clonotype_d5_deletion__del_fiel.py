# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ClonotypeRefactor'
        db.delete_table(u'clonotypes_clonotyperefactor')

        # Removing M2M table for field samples on 'AminoAcid'
        db.delete_table('clonotypes_aminoacid_samples')

        # Deleting field 'Clonotype.d5_deletion'
        db.delete_column(u'clonotypes_clonotype', 'd5_deletion')

        # Deleting field 'Clonotype.j_gene_name'
        db.delete_column(u'clonotypes_clonotype', 'j_gene_name')

        # Deleting field 'Clonotype.j_ties'
        db.delete_column(u'clonotypes_clonotype', 'j_ties')

        # Deleting field 'Clonotype.v_family_name'
        db.delete_column(u'clonotypes_clonotype', 'v_family_name')

        # Deleting field 'Clonotype.n1_index'
        db.delete_column(u'clonotypes_clonotype', 'n1_index')

        # Deleting field 'Clonotype.d_gene_name'
        db.delete_column(u'clonotypes_clonotype', 'd_gene_name')

        # Deleting field 'Clonotype.v_index'
        db.delete_column(u'clonotypes_clonotype', 'v_index')

        # Deleting field 'Clonotype.cdr3_length'
        db.delete_column(u'clonotypes_clonotype', 'cdr3_length')

        # Deleting field 'Clonotype.j_deletion'
        db.delete_column(u'clonotypes_clonotype', 'j_deletion')

        # Deleting field 'Clonotype.v_ties'
        db.delete_column(u'clonotypes_clonotype', 'v_ties')

        # Deleting field 'Clonotype.n1_insertion'
        db.delete_column(u'clonotypes_clonotype', 'n1_insertion')

        # Deleting field 'Clonotype.d_index'
        db.delete_column(u'clonotypes_clonotype', 'd_index')

        # Deleting field 'Clonotype.v_gene_name'
        db.delete_column(u'clonotypes_clonotype', 'v_gene_name')

        # Deleting field 'Clonotype.n2_index'
        db.delete_column(u'clonotypes_clonotype', 'n2_index')

        # Deleting field 'Clonotype.j_index'
        db.delete_column(u'clonotypes_clonotype', 'j_index')

        # Deleting field 'Clonotype.n2_insertion'
        db.delete_column(u'clonotypes_clonotype', 'n2_insertion')

        # Deleting field 'Clonotype.d3_deletion'
        db.delete_column(u'clonotypes_clonotype', 'd3_deletion')

        # Deleting field 'Clonotype.nucleotide'
        db.delete_column(u'clonotypes_clonotype', 'nucleotide')

        # Deleting field 'Clonotype.amino_acid'
        db.delete_column(u'clonotypes_clonotype', 'amino_acid_id')

        # Deleting field 'Clonotype.sequence_status'
        db.delete_column(u'clonotypes_clonotype', 'sequence_status')

        # Deleting field 'Clonotype.v_deletion'
        db.delete_column(u'clonotypes_clonotype', 'v_deletion')

        # Adding field 'Clonotype.rearrangement'
        db.add_column(u'clonotypes_clonotype', 'rearrangement',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['clonotypes.Rearrangement']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ClonotypeRefactor'
        db.create_table(u'clonotypes_clonotyperefactor', (
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samples.Sample'])),
            ('sequence_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('normalized_copy', self.gf('django.db.models.fields.IntegerField')()),
            ('rearrangement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.Rearrangement'])),
            ('raw_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('copy', self.gf('django.db.models.fields.IntegerField')()),
            ('normalized_frequency', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'clonotypes', ['ClonotypeRefactor'])

        # Adding M2M table for field samples on 'AminoAcid'
        db.create_table(u'clonotypes_aminoacid_samples', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aminoacid', models.ForeignKey(orm[u'clonotypes.aminoacid'], null=False)),
            ('sample', models.ForeignKey(orm[u'samples.sample'], null=False))
        ))
        db.create_unique(u'clonotypes_aminoacid_samples', ['aminoacid_id', 'sample_id'])


        # User chose to not deal with backwards NULL issues for 'Clonotype.d5_deletion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.d5_deletion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.j_gene_name'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.j_gene_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.j_ties'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.j_ties' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.v_family_name'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.v_family_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.n1_index'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.n1_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.d_gene_name'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.d_gene_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.v_index'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.v_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.cdr3_length'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.cdr3_length' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.j_deletion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.j_deletion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.v_ties'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.v_ties' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.n1_insertion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.n1_insertion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.d_index'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.d_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.v_gene_name'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.v_gene_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.n2_index'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.n2_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.j_index'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.j_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.n2_insertion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.n2_insertion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.d3_deletion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.d3_deletion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.nucleotide'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.nucleotide' and its values cannot be restored.")
        # Adding field 'Clonotype.amino_acid'
        db.add_column(u'clonotypes_clonotype', 'amino_acid',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clonotypes.AminoAcid'], null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Clonotype.sequence_status'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.sequence_status' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clonotype.v_deletion'
        raise RuntimeError("Cannot reverse this migration. 'Clonotype.v_deletion' and its values cannot be restored.")
        # Deleting field 'Clonotype.rearrangement'
        db.delete_column(u'clonotypes_clonotype', 'rearrangement_id')


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
