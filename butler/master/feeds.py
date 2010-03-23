#-*- coding:utf-8 -*-

from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings 
from butler.jobs.models import *

COMPANY_NAME = getattr(settings, 'COMPANY_NAME')

class JobsFeed(Feed):

	feed_type = Atom1Feed
	title_template = "butler/feed/job/title.html"
	description_template = "butler/feed/job/description.html"
	
	def get_object(self, bits):
		if len(bits) < 1:
			raise ObjectDoesNotExist
		application = bits[0]
		return application
			
	def title(self, obj):
		return COMPANY_NAME + ": " + unicode(obj)
	
	def link(self, obj):
		return application

	def description(self, obj):
		return "Recent %s jobs" % unicode(obj)
	
	def subtitle(self, obj):
		return self.description(obj)
		
	def items(self, obj):
		return Job.objects.filter(application=obj, status=NEW, butler__isnull=True).order_by('-pk')[:20]
	
