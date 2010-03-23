#-*- coding:utf-8 -*-

import random
import re 
from functools import wraps
from django.conf import settings 
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from libs.pubsubhubbub_publish import publish as pshb_publish

BUTLER_HUB_URL = getattr(settings, 'BUTLER_HUB_URL')

def publish(job):
	url = reverse('butler.master.views.jobs', args=[job.application])
	pshb_publish(BUTLER_HUB_URL, url)
	
	
def random_string(length):
	return ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for x in xrange(length)])



HTML_RULES = (
	(re.compile('\<br\W*\>'), '\n'),
	(re.compile('\<\/?(div|p|table|tr)>'), '\n'),
	(re.compile('\&nbsp\;'), ' '),
	(re.compile('\<.*?\>'), ''),
)
def strip_html(value):
	value = unicode(value or '')
	for pattern, replace in HTML_RULES:
		value = pattern.sub(replace, value)
	return value


def raise_form_error(form):
	for field in form:
		for error in field.errors:
			raise Exception(strip_html(unicode(error).replace('This field', unicode(field.label))))
	if isinstance(form.non_field_errors, basestring):
		raise Exception (strip_html(form.non_field_errors))
	else:
		raise Exception (strip_html(form.non_field_errors()[0]))
		

def render_to(template):
	"""
	Decorator for Django views that sends returned dict to render_to_response function
	with given template and RequestContext as context instance.

	If view doesn't return dict then decorator simply returns output.
	Additionally view can return two-tuple, which must contain dict as first
	element and string with template name as second. This string will
	override template name, given as parameter

	Parameters:

	 - template: template name to use
	"""
	def renderer(func):
		@wraps(func)
		def wrapper(request, *args, **kw):
			from django.core.exceptions import PermissionDenied
			from django.contrib.auth.decorators import login_required
			output = func(request, *args, **kw)
			context = RequestContext(request)
			context['keywords'] = kw
			context['args'] = args
			if isinstance(output, (list, tuple)):
				return render_to_response(output[1], output[0], context)
			elif isinstance(output, dict):
				return render_to_response(template, output, context)
			return output
		return wrapper
	return renderer

