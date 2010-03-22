#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.slave.worker import get_current_butler
from butler.jobs.models import ERROR 

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		butler = get_current_butler()
		job = butler.current_job
		if job:
			job.error()
			
			butler.current_job = None 
			butler.save()	
		

