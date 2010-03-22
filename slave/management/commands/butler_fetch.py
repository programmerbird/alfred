#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from slave.worker import get_current_butler

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		butler = get_current_butler()
		job = butler.get_job()
		if job:
			butler.current_job = job 
			butler.save()
			print job.pk 


		

