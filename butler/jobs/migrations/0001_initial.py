#-*- coding:utf-8 -*-

from south.db import db
from django.db import models
from butler.jobs.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Log'
        db.create_table('jobs_log', (
            ('id', orm['jobs.Log:id']),
            ('job', orm['jobs.Log:job']),
            ('butler', orm['jobs.Log:butler']),
            ('text', orm['jobs.Log:text']),
            ('created_on', orm['jobs.Log:created_on']),
        ))
        db.send_create_signal('jobs', ['Log'])
        
        # Adding model 'Butler'
        db.create_table('jobs_butler', (
            ('id', orm['jobs.Butler:id']),
            ('endpoint', orm['jobs.Butler:endpoint']),
            ('secret', orm['jobs.Butler:secret']),
            ('applications', orm['jobs.Butler:applications']),
            ('current_job', orm['jobs.Butler:current_job']),
        ))
        db.send_create_signal('jobs', ['Butler'])
        
        # Adding model 'Job'
        db.create_table('jobs_job', (
            ('id', orm['jobs.Job:id']),
            ('name', orm['jobs.Job:name']),
            ('owner', orm['jobs.Job:owner']),
            ('created_on', orm['jobs.Job:created_on']),
            ('updated_on', orm['jobs.Job:updated_on']),
            ('application', orm['jobs.Job:application']),
            ('options', orm['jobs.Job:options']),
            ('callback_url', orm['jobs.Job:callback_url']),
            ('status', orm['jobs.Job:status']),
            ('secret', orm['jobs.Job:secret']),
            ('butler', orm['jobs.Job:butler']),
        ))
        db.send_create_signal('jobs', ['Job'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Log'
        db.delete_table('jobs_log')
        
        # Deleting model 'Butler'
        db.delete_table('jobs_butler')
        
        # Deleting model 'Job'
        db.delete_table('jobs_job')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jobs.butler': {
            'applications': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_job': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'current_butler'", 'null': 'True', 'to': "orm['jobs.Job']"}),
            'endpoint': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'jobs.job': {
            'application': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'butler': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Butler']", 'null': 'True'}),
            'callback_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_owned'", 'null': 'True', 'to': "orm['auth.User']"}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'jobs.log': {
            'butler': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Butler']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['jobs']
