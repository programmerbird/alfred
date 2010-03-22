import subprocess
import random
import string
import os

def random_string(length=16):
	chars = string.letters + string.digits
	return ''.join([random.choice(chars) for i in range(length)])	
	
def execute(arguments):
	(out, err) = subprocess.Popen([ 
	"%s" % str(x) for x in arguments ], stdout=subprocess.PIPE).communicate()
	if err is not None:
		raise Exception(err)
	return out
	
def copy(source, target):
	execute(["cp", "-r", source, target])
	
def move(source, target):
	execute(["mv", source, target])

def remove(source):
	if os.path.isfile(source):
		os.remove(source)
	elif os.path.islink(source):
		os.unlink(source)
	elif os.path.isdir(source):
		for root, dirs, files in os.walk(source, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.rmdir(source)

def is_exists(path):
	return os.path.exists(path)
	
def tmpdir(directory):
	if directory[-1]=='/':
		directory = directory[:-1]
	while True:
		tmpdir = directory + random_string()
		if not os.path.exists(tmpdir):
			return tmpdir
			
def link(source, target):
	os.symlink(source, target)
	
def change_mode(source, mode):
	os.chmod(source, mode)
	
def change_owner(source, user, group=None):
	group = group or user
	os.chown(source, user, group)
	
def make_directory(target, mode=0755):
	os.makedirs(target, mode)

def access(target, mode=None):
	return os.access(target, mode)
	
def read_file(source, mode='r'):
	f = open(source, mode)
	try:
		return "\n".join(f.readlines())
	finally:
		f.close()
		
def write_file(target, content, mode='w'):
	f = open(target, 'w')
	try:
		f.write(content)
	finally:
		f.close() 

def append_file(target, content):
	write_file(target, content, 'a')	

