#-*- coding:utf-8 -*-


from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from hibird.utils import random_string


class AccessKey(models.Model):
	user = models.ForeignKey(User, primary_key=True)
	key = models.CharField(max_length=32, index=True)
	secret_key = models.CharField(max_length=32)
	
	@classmethod
	def by_user(user):
		accesskey,is_created = AccessKey.objects.get_or_create(user=user)
		return accesskey 

	def _manage_key(self):
		if not self.key:
			self.key = random_string(32)
			self.secret_key = random_string(32)
		
	def save(self, *args, **kwargs):
		self._manage_key()
		super(AccessKey, self).save(*args, **kwargs)