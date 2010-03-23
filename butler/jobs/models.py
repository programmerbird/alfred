#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson

NEW = "new"
QUEUE = "que"
PROCESS = "proc"
DONE = "done"
HOLD = "hold"
ERROR = "error"
JOB_STATUS = (
	(NEW, _("New")),
	(QUEUE, _("Assigned")),
	(HOLD, _("On hold")),
	(PROCESS, _("Processing")),
	(DONE, _("Done")),
	(ERROR, _("Error")),
)

WORKING_STATUS = (QUEUE, PROCESS,)
CLOSED_STATUS = (DONE, ERROR,)
class Job (models.Model):	
	name = models.CharField(verbose_name=_("Task name"), max_length=200)
	owner = models.ForeignKey(User, null=True, related_name="task_owned")
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	
	application = models.CharField(max_length=200, db_index=True)
	options = models.TextField(null=True, blank=True)
	callback = models.CharField(max_length=200, null=True, blank=True)
	
	status = models.CharField(max_length=10, choices=JOB_STATUS, default=NEW, editable=False)	
	
	secret = models.CharField(max_length=20, editable=False)
	butler = models.ForeignKey('Butler', null=True, editable=False)

	def _manage_secret(self):
		if not self.secret:
			self.secret = random_string(20)
			
	def _manage_name(self):
		if not self.name:
			self.name = self.application 
			
	def save(self, *args, **kwargs):
		self._manage_name()
		self._manage_secret()
		super(Job, self).save(*args, **kwargs)
		
	def publish(self):
		import publisher 
		publisher.publish(job)
		
	def json(self):
		try:
			return self._json
		except AttributeError:
			self._json = t = simplejson.loads(self.options or '{}')
			return t
			
	def complete(self):
		pass 
	
	def success(self):
		self.status = CLOSED 
		self.save()
		self.complete()
		
	def error(self):
		self.status = ERROR 
		self.save()
		self.complete()
		
	def __unicode__(self):
		return self.name 
		
class Log (models.Model):
	job = models.ForeignKey(Job, null=True, blank=True)
	butler = models.ForeignKey('Butler', null=True, blank=True)
	text = models.TextField(null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)


class Butler (models.Model):
	endpoint = models.CharField(max_length=200, db_index=True)
	secret = models.CharField(max_length=20, editable=False)
	
	applications = models.TextField(null=True, blank=True)
	current_job = models.ForeignKey(Job, null=True, blank=True, related_name='current_butler')
	
	def _manage_secret(self):
		if not self.secret:
			self.secret = random_string(20)
			
	def save(self, *args, **kwargs):
		self._manage_secret()
		super(Butler, self).save(*args, **kwargs)
		
	def get_applications(self):
		try:
			return self._applications
		except AttributeError:
			self._applications = apps = self.applications.split('\n')
			return apps 			
	
	def output(text):
		l = Log()
		l.butler = self
		l.job = self.current_job 
		l.text = text
		l.save()
			
	def _assign_job(self):
		from django.db import connection, transaction
		cursor = connection.cursor()
		application
		sql = """
			UPDATE jobs_job 
			SET butler_id=%s, status=%s 
			WHERE application IN %s
				AND status=%s
				AND butler_id IS NULL
			ORDER BY id DESC
			LIMIT 1
		"""
		cursor.execute(sql, [
			self.pk, QUEUE,
			self.get_applications(), 
			NEW,
		]) 
		transaction.set_dirty()

	def _fetch_job(self):
		if self.current_job:
			return self.current_job
		jobs = Job.objects.filter(butler=self, status__in=WORKING_STATUS).order_by('-pk')[:1]
		if jobs: 
			return jobs[0]
		
	def get_job(self):
		result = self._fetch_job()
		if not result:
			self._assign_job()
			result = self._fetch_job()
		return result 
	
