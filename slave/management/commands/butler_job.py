#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.template import Variable, Context

from slave.worker import get_current_butler

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		butler = get_current_butler()
		job = butler.get_job()
		variable = args[0]
		
		print Variable('job.%s' % variable).resolve(Context({'job': job}))


