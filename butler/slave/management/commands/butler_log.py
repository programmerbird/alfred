#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from butler.slave.worker import get_current_butler

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
	
		if args:
			data = ' '.join(args)
		else:
			import sys 
			lines = sys.stdin.readlines()
			data = '\n'.join(lines)
		
		if data:
			butler = get_current_butler()
			butler.output(data)
		

