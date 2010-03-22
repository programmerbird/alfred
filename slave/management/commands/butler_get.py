#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.template import Variable, Context
from django.conf import settings 

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		variable = args[0]
		job = None
		if job:
			try:
				butler = get_current_butler()
				job = butler.current_job
			except:
				pass 
		print Variable(variable).resolve(Context({
			'settings': settings,
			'job': job,
		}))


