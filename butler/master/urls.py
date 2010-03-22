#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *
from views import JobsFeed

urlpatterns = patterns('',
	('(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': 
		'job': JobsFeed,		
	}),
)

