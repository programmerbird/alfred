#-*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.conf import settings

import worker

BUTLER_APPLICATIONS = getattr(settings, 'BUTLER_APPLICATIONS', [])
def callback(request, application):
	if request.method == 'GET':
		mode = request.GET['hub.mode']
		topic = request.GET['hub.topic']
		challenge = request.GET['hub.challenge']
		lease_seconds = request.GET.get('hub.lease_seconds')
		verify_token = request.GET.get('hub.verify_token', '')
		if mode == 'subscribe':
			if application not in BUTLER_APPLICATIONS:
				raise Http404 
			if verify_token != worker.get_application_key(application):
				raise Http404
		return HttpResponse(challenge, content_type='text/plain')
	elif request.method == 'POST':
		worker.start_worker()
		return HttpResponse('')
	return Http404

