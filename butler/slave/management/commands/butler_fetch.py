#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.conf import settings
from butler.slave.worker import get_current_butler
import os 

BUTLER_APPS_DIRECTORY = getattr(settings, 'BUTLER_APPS_DIRECTORY')

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		butler = get_current_butler()
		job = butler.get_job()
		if not job: 
			return
		if butler.current_job != job:
			butler.current_job = job 
			butler.save()
		print os.path.join(BUTLER_APPS_DIRECTORY, job.application)



		

