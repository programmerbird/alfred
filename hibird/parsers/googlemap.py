#-*- coding:utf-8 -*-
from django.conf import settings
import re 

MAP_WIDTH = getattr(settings, 'MAP_WIDTH', 560)
MAP_HEIGHT = getattr(settings, 'MAP_HEIGHT', 340)

def googlemap_pre(matches):
	query = matches.group(1)
	return "[googlemap:%s]" % query
	
def googlemap(matches):
	query = matches.group(1)
	query = query.replace('&amp;', '&')
	query = query.replace('&amp;', '&')
	if '&quot;' in query:
		query = query.split('&quot;',1)[0]
	if '&output=' in query:
		query = re.sub(r'output=[a-z]*', 'output=embed', query)
	else:
		query = query + '&output=embed'
	external_query = query.replace('output=embed', 'source=embed')
	width = MAP_WIDTH
	height = MAP_HEIGHT
	return """<iframe width="%(width)d" height="%(height)d" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" 
	src="http://maps.google.com/%(query)s">
	</iframe><br /><small><a href="http://maps.google.com/%(external_query)s" style="color:#0000FF;text-align:left">View Larger Map</a></small>""" % locals()
	
PRE_OBJECT_LINKS = (
	(re.compile(r'\&lt\;iframe.*?maps\.google\.com\/(\?ie\=UTF8[^\s\[\]\<\"]*).*?\&lt\;\/iframe\&gt\;.*?View Larger Map\&lt\;\/a\&gt\;\&lt\;\/small\&gt\;', re.DOTALL), googlemap_pre),
	(re.compile(r'\&lt\;iframe.*?maps\.google\.com\/(\?ie\=UTF8[^\s\[\]\<\"]*).*?\&lt\;\/iframe\&gt\;', re.DOTALL), googlemap_pre),
	(re.compile(r'\<iframe.*?maps\.google\.com\/(\?ie\=UTF8[^\s\[\]\<\"]*).*?\<\/iframe\>.*?View Larger Map\<\/a\>\<\/small\>', re.DOTALL), googlemap_pre),
	(re.compile(r'\<iframe.*?maps\.google\.com\/(\?ie\=UTF8[^\s\[\]\<\"]*).*?\<\/iframe\>', re.DOTALL), googlemap_pre),
	(re.compile(r'http\:\/\/[^\s]*?maps\.google\.com\/(\?ie\=UTF8[^\s\[\]\<\"]*)'), googlemap_pre),
	(re.compile(r'\<a[^\>]*?href=\"\[googlemap:([^\]]+)\]\"[^\>]*?\>\[googlemap\:([^\]]+)\]\<\/a\>'), r'[googlemap:\1]'),
)
PRE_OBJECT_PATTERN = re.compile(r'\[googlemap:([^\]]+)\]')
OBJECT_LINKS = PRE_OBJECT_LINKS + (
	(PRE_OBJECT_PATTERN, googlemap),	
)

	
def parse(txt):
	for pattern, replacement in OBJECT_LINKS:
		txt = pattern.sub(replacement, txt)
	return txt 
	
def main():
	testcases = """
<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" 
src="http://maps.google.com/?ie=UTF8&amp;hq=&amp;hnear=Mahidol+University,+Thung+Phaya+Thai,+Ratchathewi,+Bangkok+10400,+Thailand&amp;ll=13.74543,100.542068&amp;spn=0.029889,0.045447&amp;t=h&amp;z=15&amp;output=embed">
</iframe>


http://maps.google.com/?ie=UTF8&hq=&hnear=Mahidol+University,+Thung+Phaya+Thai,+Ratchathewi,+Bangkok+10400,+Thailand&ll=13.74543,100.542068&spn=0.029889,0.045447&t=h&z=15


<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/?ie=UTF8&amp;hq=&amp;hnear=Mahidol+University,+Thung+Phaya+Thai,+Ratchathewi,+Bangkok+10400,+Thailand&amp;t=h&amp;ll=13.74543,100.542068&amp;spn=0.009213,0.007682&amp;z=15&amp;output=embed"></iframe>
<br /><small><a href="http://maps.google.com/?ie=UTF8&amp;hq=&amp;hnear=Mahidol+University,+Thung+Phaya+Thai,+Ratchathewi,+Bangkok+10400,+Thailand&amp;t=h&amp;ll=13.74543,100.542068&amp;spn=0.009213,0.007682&amp;z=15&amp;source=embed" style="color:#0000FF;text-align:left">View Larger Map</a></small>

	""".split('\n\n\n')
	for x in testcases:
		for pattern, replacement in OBJECT_LINKS:
			x = pattern.sub(replacement, x)

	print "MARKDOWN"
	import markdown
	for x in testcases:
		x = markdown.markdown(x, safe_mode="escape")
		for pattern, replacement in OBJECT_LINKS:
			x = pattern.sub(replacement, x)
		print "---<hr />"
		print x 

if __name__ == '__main__':
	import sys
	sys.exit(main())






