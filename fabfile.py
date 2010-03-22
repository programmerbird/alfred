#-*- coding:utf-8 -*-
from fabric.api import *

env.roledefs = {
	'test': ['127.0.0.1',],
}

env.hosts = env.roledefs['test']
env.settings = 'settings'

def bootstrap():
	local('virtualenv --no-site-packages env', capture=False)
	local('env/bin/pip install -r requirements.ini', capture=False)
	
def migrate():
	run('%(env_home)s/bin/python %(home)s/manage.py syncdb --settings=%(settings)s' % env)
	run('%(env_home)s/bin/python %(home)s/manage.py migrate --settings=%(settings)s' % env)
	
def diagram():
	local('/usr/bin/python manage.py gendiagram tib hotel billing -o resource/er.png')
