#-*- coding:utf-8 -*-

from django.conf import settings
from urllib import urlencode
import urllib2


from functools import wraps
from django.template import RequestContext
from django.shortcuts import render_to_response

LEASE_SECONDS = getattr(settings, 'PUBSUBHUBBUB_LEASE_SECONDS', 2592000)  # 30 days in seconds

def _send_request(url, data):
    def data_generator():
        for key, value in data.items():
            key = 'hub.' + key
            if isinstance(value, (basestring, int)):
                yield key, str(value)
            else:
                for subvalue in value:
                    yield key, value
    encoded_data = urlencode(list(data_generator()))
    return urllib2.urlopen(url, encoded_data)


def subscribe(hub=None, topic=None, callback=None,
              lease_seconds=None, verify_token=None):
    if hub is None:
        raise TypeError(
            'hub cannot be None if the feed does not provide it')

    if lease_seconds is None:
        lease_seconds = LEASE_SECONDS

    response = _send_request(hub, {
            'mode': 'subscribe',
            'callback': callback,
            'topic': topic,
            'verify': ('async', 'sync'),
            'verify_token': verify_token,
            'lease_seconds': lease_seconds,
            })

    info = response.info()
    if info.status == 204:
    	# verified
    	return True
    elif info.status == 202: # async verification
    	# not verified yet
    	return False
    else:
        error = response.read()
        raise urllib2.URLError('error subscribing to %s on %s:\n%s' % (
                topic, hub, error))


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
