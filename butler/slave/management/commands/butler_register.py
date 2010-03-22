#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.jobs.worker import register, start_worker

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		register()
		start_worker()

