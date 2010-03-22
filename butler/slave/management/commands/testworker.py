#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.slave.worker import get_current_butler, start_worker

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		start_worker()

