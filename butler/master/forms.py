#-*- coding:utf-8 -*-

import hashlib

from django import forms
from django.utils.translation import ugettext_lazy as _
from models import *
from butler.jobs.models import Job

class JobForm (forms.ModelForm):
	key = forms.CharField()
	token = forms.CharField()
	
	def clean_token(self):
		key = self.cleaned_data.get('key')
		token = self.cleaned_data.get('token')
		app = self.cleaned_data.get('application')
		options = self.cleaned_data.get('options')
		token = self.cleaned_data.get('token')
		
		try:
			access_key = AccessKey.objects.get(key=key)
		except AccessKey.DoesNotExist:
			raise forms.ValidationError('Invalid Key')
			
		if not Authorization.exists(user=access_key.user, application=app):
			raise forms.ValidationError('Permission Denied: [%s-%s]' % (access_key.user.username, app))
			
		secret = '%s!%s!%s' % (access_key.secret, app, options)
		if token != hashlib.sha1(secret).hexdigest():
			raise forms.ValidationError('Invalid Token')
		
	class Meta:
		model = Job
		fields = ('application', 'options', 'callback',)
		

