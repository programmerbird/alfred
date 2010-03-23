#-*- coding:utf-8 -*-

import hashlib 

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from utils import random_string

class AccessKey(models.Model):
	user = models.ForeignKey(User, primary_key=True, editable=False)
	key = models.CharField(max_length=32, unique=True)
	secret_key = models.CharField(max_length=32)
	
	def check_sum(self, txt):
		token = "%s!%s" % (self.secret_key, txt)
		return hashlib.sha1(token).hexdigest()
		
	@classmethod
	def by_user(cls, user):
		accesskey,is_created = AccessKey.objects.get_or_create(user=user)
		return accesskey 

	def _manage_key(self):
		if not self.key:
			self.key = random_string(32)
			self.secret_key = random_string(32)
		
	def save(self, *args, **kwargs):
		self._manage_key()
		super(AccessKey, self).save(*args, **kwargs)
		
class Authorization(models.Model):	
	user = models.ForeignKey(User, db_index=True)
	application = models.CharField(max_length=200)
	created_on = models.DateTimeField(auto_now_add=True)
	
	@classmethod
	def exists(cls, user, application):
		if user.is_superuser:
			return True 
		else:
			records = Authorization.objects.filter(user=user, application=application)
			if records:
				return True 
			return False

