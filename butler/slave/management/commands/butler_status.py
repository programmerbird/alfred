#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.slave.worker import get_current_butler

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		butler = get_current_butler()
		job = butler.current_job
		if job:
			job.status = args[0]
			job.save()

