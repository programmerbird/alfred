#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('butler.slave.views',
	('^callback/(?P<application>[\w\-]+)/?', 'callback'),
	('^debug/$', 'debug'),
)

