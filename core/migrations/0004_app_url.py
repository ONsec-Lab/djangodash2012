# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Inst.url'
        db.add_column('core_inst', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Inst.url'
        db.delete_column('core_inst', 'url')


    models = {
        'core.inst': {
            'Meta': {'object_name': 'Inst'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ouruser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OurUser']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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