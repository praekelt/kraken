# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Request.order'
        db.add_column(u'kraken_request', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Request.order'
        db.delete_column(u'kraken_request', 'order')


    models = {
        u'kraken.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'phase_duration': ('django.db.models.fields.IntegerField', [], {}),
            'phase_rate': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'kraken.request': {
            'Meta': {'ordering': "['id']", 'object_name': 'Request'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dyn_variable': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'http_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kraken.Profile']"}),
            'think_time': ('django.db.models.fields.IntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'kraken.server': {
            'Meta': {'object_name': 'Server'},
            'cores': ('django.db.models.fields.IntegerField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'kraken.test': {
            'Meta': {'ordering': "['-test_time']", 'object_name': 'Test'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kraken.Profile']"}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stdout': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'task_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'test_log': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'test_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'kraken.useragent': {
            'Meta': {'ordering': "['probability']", 'object_name': 'UserAgent'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kraken.UserAgents']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.IntegerField', [], {}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kraken.Profile']"})
        },
        u'kraken.useragents': {
            'Meta': {'object_name': 'UserAgents'},
            'agent': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['kraken']