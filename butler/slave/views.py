#-*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.conf import settings
from utils import render_to
import worker

BUTLER_MASTER_URL = getattr(settings, 'BUTLER_MASTER_URL')

def callback(request, application):
	if request.method == 'GET':
		mode = request.GET['hub.mode']
		topic = request.GET['hub.topic']
		challenge = request.GET['hub.challenge']
		lease_seconds = request.GET.get('hub.lease_seconds')
		verify_token = request.GET.get('hub.verify_token', '')
		if mode == 'subscribe':
			from worker import get_applications
			applications = get_applications()
			if application not in applications:
				raise Http404 
			if verify_token != worker.get_application_key(application):
				raise Http404
		return HttpResponse(challenge, content_type='text/plain')
	elif request.method == 'POST':
		worker.start_worker()
		return HttpResponse('')
	return Http404

@render_to('butler/job/debug.html')
def debug(request):
	if request.method == 'POST':
		worker.start_worker()
	butler = worker.get_current_butler()
	job = butler.current_job 
	applications = worker.get_applications()
	
	post_url = BUTLER_MASTER_URL + "new/job/"
	return locals()
