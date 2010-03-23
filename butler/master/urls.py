#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *
from admin import butler_admin
from feeds import JobsFeed

urlpatterns = patterns('',
	('^admin/', include(butler_admin.urls)),
	('^new/job/', 'butler.master.views.new_job'),
	('^job/(?P<job_id>\d+)/$', 'butler.master.views.job'),
	('(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {
		'feed_dict': {
			'job': JobsFeed
		},		
	}),
)

