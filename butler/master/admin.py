#-*- coding:utf-8 -*-
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
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
			
butler_admin = ButlerAdminSite()
butler_admin.register(User, ButlerUserAdmin)
butler_admin.register(Group, GroupAdmin)

