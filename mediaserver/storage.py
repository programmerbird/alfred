#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.files.storage import FileSystemStorage
from django.conf import settings

MEDIA_UPLOAD_URL = getattr(settings, 'MEDIA_UPLOAD_URL', getattr(settings, 'MEDIA_URL'))

class ExternalMediaStorage(FileSystemStorage):
	def __init__(self, base_url=None, *args, **kwargs):
		super(ExternalMediaStorage, self).__init__(base_url=MEDIA_UPLOAD_URL, *args, **kwargs)
