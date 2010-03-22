#-*- coding:utf-8 -*-

from hibird.utils import uri 
from django.conf import settings 
from libs.pubsubhubbub_publish import publish as pshb_publish
from jobs.models import *

JOBS_HUB_URL = getattr(settings, JOBS_HUB_URL)
def publish(job):
	url = uri('jobs.views.jobs_feed', [job.application])
	pshb_publish(JOBS_HUB_URL, url)
	
def jobs_feed(request, application):
	jobs = Job.objects.filter(application=application).order_by('-pk')
	return locals()
	
