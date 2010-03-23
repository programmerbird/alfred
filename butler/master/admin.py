#-*- coding:utf-8 -*-
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from butler.jobs.models import Job, Butler, Log
from models import * 


class ButlerAdminSite(AdminSite):
	pass 
	
	
class AccessKeyInline(admin.TabularInline):
	model = AccessKey
	fk_name = "user"

class AuthorizationInline(admin.TabularInline):
	model = Authorization
	fk_name = "user"

class ButlerUserAdmin(UserAdmin):
	actions = ['generate_access_key',]
	inlines = [
		AccessKeyInline,
		AuthorizationInline,
	]
	def generate_access_key(self, request, queryset):
		for user in queryset:
			AccessKey.by_user(user)
		self.message_user(request, "Successfully generated accesskey.")
			
class JobAdmin(admin.ModelAdmin):
	list_display = ('application', 'options', 'status', 'butler',)

class LogAdmin(admin.ModelAdmin):
	list_display = ('job', 'butler','created_on', )
	search_fields = ('job__id', )
	
butler_admin = ButlerAdminSite()
butler_admin.register(User, ButlerUserAdmin)
butler_admin.register(Group, GroupAdmin)
butler_admin.register(Job, JobAdmin)
butler_admin.register(Butler)
butler_admin.register(Log, LogAdmin)

