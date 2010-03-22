#-*- coding:utf-8 -*-

from django.conf import settings
from urllib import urlencode
import urllib2

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

