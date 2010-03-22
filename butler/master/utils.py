#-*- coding:utf-8 -*-

import random
from django.conf import settings 
from django.core.urlresolvers import reverse

from libs.pubsubhubbub_publish import publish as pshb_publish

BUTLER_HUB_URL = getattr(settings, 'BUTLER_HUB_URL')

def publish(job):
	url = reverse('butler.master.views.jobs', args=[job.application])
	pshb_publish(BUTLER_HUB_URL, url)
	
	
def random_string(length):
	return ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for x in xrange(length)])

