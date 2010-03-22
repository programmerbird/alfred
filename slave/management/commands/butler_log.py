#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from slave.worker import get_current_butler

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		import sys 
		lines = sys.stdin.readlines()
		data = '\n'.join(lines)
		
		butler = get_current_butler()
		butler.output(data)
		

