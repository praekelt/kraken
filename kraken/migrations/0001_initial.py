# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Server'
        db.create_table(u'kraken_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('cores', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'kraken', ['Server'])

        # Adding model 'Profile'
        db.create_table(u'kraken_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phase_duration', self.gf('django.db.models.fields.IntegerField')()),
            ('phase_rate', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'kraken', ['Profile'])

        # Adding model 'UserAgents'
        db.create_table(u'kraken_useragents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('agent', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'kraken', ['UserAgents'])

        # Adding model 'UserAgent'
        db.create_table(u'kraken_useragent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kraken.Profile'])),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kraken.UserAgents'])),
            ('probability', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'kraken', ['UserAgent'])

        # Adding model 'Request'
        db.create_table(u'kraken_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kraken.Profile'])),
            ('http_auth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('think_time', self.gf('django.db.models.fields.IntegerField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dyn_variable', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'kraken', ['Request'])

        # Adding model 'Test'
        db.create_table(u'kraken_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kraken.Profile'])),
            ('test_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('running', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('test_log', self.gf('django.db.models.fields.TextField')(default='')),
            ('stdout', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'kraken', ['Test'])


    def backwards(self, orm):
        # Deleting model 'Server'
        db.delete_table(u'kraken_server')

        # Deleting model 'Profile'
        db.delete_table(u'kraken_profile')

        # Deleting model 'UserAgents'
        db.delete_table(u'kraken_useragents')

        # Deleting model 'UserAgent'
        db.delete_table(u'kraken_useragent')

        # Deleting model 'Request'
        db.delete_table(u'kraken_request')

        # Deleting model 'Test'
        db.delete_table(u'kraken_test')


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