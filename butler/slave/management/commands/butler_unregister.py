#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.slave.worker import unregister

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		unregister()

