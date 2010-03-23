#-*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
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
			if form.is_valid():
				n = form.save(commit=False)
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

def job(request, job_id):
	pass 
	
