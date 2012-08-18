# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Inst'
        db.delete_table('core_inst')

        # Deleting model 'OurUser'
        db.delete_table('core_ouruser')

        # Adding model 'Instance'
        db.create_table('core_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=10)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('core', ['Instance'])


    def backwards(self, orm):
        # Adding model 'Inst'
        db.create_table('core_inst', (
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=10)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ouruser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.OurUser'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Inst'])

        # Adding model 'OurUser'
        db.create_table('core_ouruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['OurUser'])

        # Deleting model 'Instance'
        db.delete_table('core_instance')


    models = {
        'core.instance': {
            'Meta': {'object_name': 'Instance'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'core.step': {
            'Meta': {'object_name': 'Step'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'file_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tutorial']"})
        },
        'core.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'app_name': ('django.db.models.fields.CharField', [], {'default': "'hellodjango'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']