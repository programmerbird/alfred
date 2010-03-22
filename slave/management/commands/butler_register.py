#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from jobs.worker import register

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		register()

