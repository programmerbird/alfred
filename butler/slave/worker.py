#-*- coding:utf-8 -*-
#-*- coding:utf-8 -*-

import hashlib 

from django.conf import settings 
from django.core.urlresolvers import reverse
from butler.jobs import models 

SETTINGS_MODULE = getattr(settings, 'SETTINGS_MODULE', 'settings')

BUTLER_MANAGE_DIRECTORY = getattr(settings, 'BUTLER_MANAGE_DIRECTORY')
BUTLER_VIRTUALENV = getattr(settings, 'BUTLER_VIRTUALENV')
BUTLER_APPS_DIRECTORY = getattr(settings, 'BUTLER_APPS_DIRECTORY', '/home/alfred/apps')
BUTLER_LEASE_SECONDS = getattr(settings, 'BUTLER_LEASE_SECONDS', 259200) # 3 days in seconds

SITE_URL = getattr(settings, 'SITE_URL')
SECRET_KEY = getattr(settings, 'SECRET_KEY')
BUTLER_HUB_URL = getattr(settings, 'BUTLER_HUB_URL', '')
BUTLER_MASTER_URL = getattr(settings, 'BUTLER_MASTER_URL', '')

def get_application_key(application):
	txt = (application + SECRET_KEY)
	return hashlib.sha1(txt).hexdigest()
	
def get_endpoint():
	return SITE_URL
	
def get_applications():
	import os
	apps = [x for x in os.listdir(BUTLER_APPS_DIRECTORY) if x and x[:1] not in ('.','_',) and x[-1:] not in ('~',)]
	apps.sort()
	return apps 

def register():
	endpoint = get_endpoint()
	butler, is_created = models.Butler.objects.get_or_create(endpoint=endpoint)
	
	apps = '\n'.join(get_applications())
	butler.applications = apps
	butler.save()
	
	# pubsubhubbub subscribe!
	from utils import subscribe 
	for app in apps:
		app_url = BUTLER_MASTER_URL + 'job/' + app 
		app_key = get_application_key(app)
		callback_url = reverse('butler.slave.views.callback', args=[app])
		subscribe(hub=BUTLER_HUB_URL, topic=app_url, callback=callback_url, 
			lease_seconds=BUTLER_LEASE_SECONDS, verify_token=app_key)
	return butler
	
	
def unregister(butler=None):
	endpoint = get_endpoint()
	butler, is_created = models.Butler.objects.get_or_create(endpoint=endpoint)
	butler.applications = ''
	butler.save()

	return butler
	
	
def get_current_butler():
	endpoint = get_endpoint()
	butler, is_created = models.Butler.objects.get_or_create(endpoint=endpoint)
	return butler
	
def start_worker():
	import os, subprocess 
	daemon = os.path.abspath(os.path.join(__file__, '../bin/start-butler-daemon.sh'))
	subprocess.Popen(['/bin/sh', daemon, BUTLER_VIRTUALENV, BUTLER_MANAGE_DIRECTORY, SETTINGS_MODULE]).communicate(0)

