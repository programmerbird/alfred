#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.db.models.query_utils import CollectedObjects

LOOP = 20
class Command(NoArgsCommand):
	help = "Runs a Python interactive interpreter. Tries to use IPython, if it's available."

	requires_model_validation = True

	def handle_noargs(self, **options):
		from django.db.models import get_apps, get_models

		print "       CHECKING CASCADE DELETE"
		for app in get_apps():
			loaded_models = get_models(app)
			print "%30s"  % app.__name__.upper().replace('.MODELS','')
			for x in loaded_models:
				model_name = unicode(x._meta.verbose_name).title()
				print "%30s :" % model_name, 
				seen_count = 0
				seen_types = []
				try:
					while 1:
						objs = x.objects.all().order_by('?')[:LOOP]
						seen_objs = CollectedObjects()
						for obj in objs:
							obj._collect_sub_objects(seen_objs, nullable=False)
				
						seen_types = []
						for seen_cls, seen_objs in seen_objs.items():
							if seen_cls not in seen_types:
								seen_types.append(seen_cls)

						if len(seen_types)==seen_count:
							break
						seen_count = len(seen_types)
					print [ x.__name__ for x in seen_types ]
				except Exception, e:
					print unicode(e)
			print ""
			print ""

