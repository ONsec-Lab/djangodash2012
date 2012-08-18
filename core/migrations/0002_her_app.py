# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OurUser'
        db.create_table('core_ouruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['OurUser'])

        # Adding model 'Inst'
        db.create_table('core_inst', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=10)),
        ))
        db.send_create_signal('core', ['Inst'])


    def backwards(self, orm):
        # Deleting model 'OurUser'
        db.delete_table('core_ouruser')

        # Deleting model 'Inst'
        db.delete_table('core_inst')


    models = {
        'core.inst': {
            'Meta': {'object_name': 'Inst'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'})
        },
        'core.ouruser': {
            'Meta': {'object_name': 'OurUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.step': {
            'Meta': {'object_name': 'Step'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tutorial']"})
        },
        'core.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']