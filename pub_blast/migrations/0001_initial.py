# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlastQuery'
        db.create_table(u'pub_blast_blastquery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
        ))
        db.send_create_signal(u'pub_blast', ['BlastQuery'])


    def backwards(self, orm):
        # Deleting model 'BlastQuery'
        db.delete_table(u'pub_blast_blastquery')


    models = {
        u'pub_blast.blastquery': {
            'Meta': {'object_name': 'BlastQuery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'})
        }
    }

    complete_apps = ['pub_blast']