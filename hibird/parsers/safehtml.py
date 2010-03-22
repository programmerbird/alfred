#-*- coding:utf-8 -*-
import sgmllib, string
import re

class StrippingParser(sgmllib.SGMLParser):

	# These are the HTML tags that we will leave intact
	valid_tags = ('b', 'a', 'i', 'br', 'p', 'strong', 'span', 'img', 'ul', 'ol', 'li', 'u', 
		'table','tr','td','tbody', 'thead','col', 'font','blockquote','div')

	from htmlentitydefs import entitydefs # replace entitydefs from sgmllib
	
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		self.result = ""
		self.endTagList = [] 
		
	def handle_data(self, data):
		if data:
			self.result = self.result + data

	def handle_charref(self, name):
		self.result = "%s&#%s;" % (self.result, name)
		
	def handle_entityref(self, name):
		if self.entitydefs.has_key(name): 
			x = ';'
		else:
			# this breaks unstandard entities that end with ';'
			x = ''
		self.result = "%s&%s%s" % (self.result, name, x)
	
	def unknown_starttag(self, tag, attrs):
		""" Delete all tags except for legal ones """
		if tag in self.valid_tags:	   
			self.result = self.result + '<' + tag
			for k, v in attrs:
				if string.lower(k[0:2]) != 'on' and string.lower(v[0:10]) != 'javascript':
					self.result = '%s %s="%s"' % (self.result, k, v)
			endTag = '</%s>' % tag
			self.endTagList.insert(0,endTag)	
			self.result = self.result + '>'
				
	def unknown_endtag(self, tag):
		if tag in self.valid_tags:
			self.result = "%s</%s>" % (self.result, tag)
			remTag = '</%s>' % tag
			self.endTagList.remove(remTag)

	def cleanup(self):
		""" Append missing closing tags """
		for j in range(len(self.endTagList)):
				self.result = self.result + self.endTagList[j]	
		


	
urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('(\s|\<p\>)(http:\/\/\S+)')
def urlify_html(value):
	value = urlfinder.sub(r'<a href="\1">\1</a>', value)
	return urlfinder2.sub(r'<a href="\2">\2</a>', value)
	
	
def parse(s):
	""" Strip illegal HTML tags from string s """
	parser = StrippingParser()
	parser.feed(s)
	parser.close()
	parser.cleanup()
	value = urlify_html(parser.result)
	return value

