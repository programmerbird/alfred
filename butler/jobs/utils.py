#-*- coding:utf-8 -*-

import random
	
def random_string(length):
	return ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for x in xrange(length)])

