# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tutorial'
        db.create_table('core_tutorial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('core', ['Tutorial'])

        # Adding model 'Step'
        db.create_table('core_step', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('num', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('tutorial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tutorial'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Step'])


    def backwards(self, orm):
        # Deleting model 'Tutorial'
        db.delete_table('core_tutorial')

        # Deleting model 'Step'
        db.delete_table('core_step')


    models = {
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