#-*- coding:utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
import os

# [butler]
urlpatterns = patterns('', 
	('^slave/', include('butler.slave.urls')),
	('', include('butler.master.urls')),
)

# [admin]
from django.contrib import admin
admin.autodiscover()
urlpatterns += patterns('', (r'^admin/(.*)', admin.site.root),)

# [debug]  
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'media')}),
	)

