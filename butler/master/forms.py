#-*- coding:utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from models import *
from butler.jobs.models import Job

class JobForm (forms.ModelForm):
	key = forms.CharField(required=False)
	token = forms.CharField(required=False)
	
	def clean_token(self):
		key = self.cleaned_data.get('key')
		token = self.cleaned_data.get('token')
		app = self.cleaned_data.get('application')
		options = self.cleaned_data.get('options')
		token = self.cleaned_data.get('token')
		
		if not key:
			if self.user.is_authenticated():
				access_key = AccessKey.by_user(self.user)
				key = access_key.key 
				token = access_key.check_sum(app + options)
			else:
				raise forms.ValidationError('Invalid Key')
		try:
			access_key = AccessKey.objects.get(key=key)
		except AccessKey.DoesNotExist:
			raise forms.ValidationError('Invalid Key')
			
		self.user = access_key.user
			
		if not Authorization.exists(user=access_key.user, application=app):
			raise forms.ValidationError('Permission Denied: [%s-%s]' % (access_key.user.username, app))
			
		if token != access_key.check_sum(app + options):
			raise forms.ValidationError('Invalid Token')
		
	class Meta:
		model = Job
		fields = ('application', 'options', 'callback',)
		

