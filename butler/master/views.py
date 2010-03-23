#-*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.conf import settings
from butler.jobs.models import Job
from models import *
import forms 
from utils import render_to, raise_form_error
	
@render_to('butler/job/new.html')
def new_job(request):
	try:
		output = request.GET.get('output')
		if request.method=='GET':
			form = forms.JobForm()
			
		if request.method=='POST':
			form = forms.JobForm(data=request.POST)
			form.user = request.user
			if form.is_valid():
				n = form.save(commit=False)
				n.owner = form.user
				n.save()
				return HttpResponse(simplejson.dumps({
					'pk': n.pk, 
					'secret': n.secret, 
					'status': n.status,
				}))
			else:
				if output != 'form':
					raise_form_error(form)
	except Exception, e:
		error = unicode(e)
		if output == 'form':
			form.non_fields_error = error
		else:
			return HttpResponse(simplejson.dumps({
				'error': unicode(e), 
			}), status=400)
		
	return locals()

def get_job(request, job_id):
	try:
		job = Job.objects.get(pk=job_id)
	except Job.DoesNotExist:
		raise Http404
	if request.user.is_authenticated():
		if job.owner == request.user:
			return job
	token = request.GET.get('token')
	access_key = AccessKey.by_user(job.owner)
	if access_key.check_sum(request.path) != token:
		raise Exception("Invalid Token")
	return job 	

def job(request, job_id):
	job = get_job(request, job_id)
	job_meta = serializers.serialize('python', [job])[0] 
	fields = job_meta['fields']
	fields['pk'] = job_meta['pk']
	return HttpResponse(simplejson.dumps(fields, cls=DjangoJSONEncoder))

