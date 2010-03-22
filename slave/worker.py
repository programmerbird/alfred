#-*- coding:utf-8 -*-
#-*- coding:utf-8 -*-

import hashlib 

from django.conf import settings 
from jobs import models 

BUTLER_SETTINGS = getattr(settings, 'BUTLER_SETTINGS', 'settings')
BUTLER_SECRET = getattr(settings, 'BUTLER_SECRET', '')
BUTLER_ENDPOINT = getattr(settings, 'BUTLER_ENDPOINT', '')
BUTLER_APPS_DIRECTORY = getattr(settings, 'BUTLER_APPS_DIRECTORY', '/home/alfred/apps')

def get_application_key(application):
	txt = (application + BUTLER_SECRET)
	return hashlib.md5(txt).hexdigest()
	
def get_endpoint():
	return BUTLER_ENDPOINT 
	
def get_applications():
	import os
	apps = [x for x in os.listdir(BUTLER_APPS_DIRECTORY) if x and x[:1] not in ('.', '_')]
	apps.sort()
	return apps 

def register():
	endpoint = get_endpoint()
	butler, is_created = Butler.objects.get_or_create(endpoint=endpoint)
	butler.applications = '\n'.join(get_applications())
	butler.save()
	
	#TODO: pubsubhubbub subcribe!
	return butler
	
def unregister(butler=None):
	endpoint = get_endpoint()
	butler, is_created = Butler.objects.get_or_create(endpoint=endpoint)
	butler.applications = ''
	butler.save()

	#TODO: pubsubhubbub unsubcribe!
	return butler
	
	
def get_current_butler():
	endpoint = get_endpoint()
	butler, is_created = Butler.objects.get_or_create(endpoint=endpoint)
	return butler
	
def start_worker():
	import os, subprocess 
	daemon = os.path.abspath(os.path.join(__file__, '../bin/start-butler-daemon.sh'))
	subprocess.Popen(['/bin/sh', daemon, BUTLER_SETTINGS]).communicate(0)

