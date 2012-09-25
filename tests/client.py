#!/usr/bin/env python3

from mmodule_sms import *

s = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <count n="1">10</count>
    <data><id>491691</id><name>test</name></data>
    <data><id>491692</id><name>test2</name></data>
    <data><id>503938</id><name>hello, world</name></data>
</result>"""

from urllib import urlencode
from httplib import HTTPConnection
from xml.dom.minidom import parseString
from mmodules.xmlpolymerase.odict import OrderedDict
from mmodules.xmlpolymerase.serializer import serialize
from mmodules.xmlpolymerase.deserializer import deserialize

def uni2hex(uni):
	return ''.join([x.encode('hex').zfill(4) for x in uni])

def uni2uhex(uni):
	u = ''
	for x in uni:
		try:
			u += x.encode('hex').zfill(4)
		except:
			u += x.encode('unicode_escape').lstrip('\u').zfill(4)
	return u

def main():
	
	
# 	import datetime
# 
# 
# 	print datetime.datetime.now()
# 
# 	from datetime import datetime
# 	print datetime.now()
# 
# 
# 	return
# 
# 	print "Today is day", time.localtime()[7], "of the current year" 
# 	# Today is day 218 of the current year
# 
# 	today = datetime.date.today()
# 	print "Today is day", today.timetuple()[7], "of ", today.year
# 	# Today is day 218 of 2003
# 
# 	print "Today is day", today.strftime("%j"), "of the current year" 
# 	# Today is day 218 of the current year
# 	
# 	return
# 	
# 	# import time
# 	import datetime
# 
# 	print datetime.date(datetime.time())
# 	
# 	# now = datetime.datetime.fromtimestamp(EpochSeconds)
# 	# #or use datetime.datetime.utcfromtimestamp()
# 	# print now
# 	# #=> datetime.datetime(2003, 8, 6, 20, 43, 20)
# 	# print now.ctime()
# 	
# 	with open('pushing.sh', 'r') as f:
# 		body = f.read()
# 	print body
# 	return body
# 	
# 	
# 	for cmd, desc in HELP:
# 		print '%s = %s' % (cmd, desc)
# 
# 	print
# 	
# 	for line in HELP:
# 		print '%s = %s' % line
# 
# 	print
# 
# 	for line in HELP:
# 		print '%-10s = %s' % line
# 
# 	print
# 
# 	print ''.join(['%-10s = %s\n' % x for x in HELP])
# 
# 	return
# 	
# 	s1 = '2€'
# 	u1 = u'2€'
# 	print uni2hex(s1)
# 	print uni2uhex(u1)
# 
# 	s2 = 'selling iphone for 200€, العربية'
# 	u2 = u'selling iphone for 200€, العربية'
# 	print uni2hex(s2)
# 	print uni2uhex(u2)
# 	
# 	s3 = '''\
# I358:اليونان تحيي أمل التأهل وتقلص فرصة "نسور"ة"
# I357:مظاهرات حاشدة ليهود متشددين دفاعاً عن "العنصرية"
# I356:روسيا تنتقد عقوبات أمريكية أوروبية "أحادية" على إيران\
# '''
# 
# 	u3 = u'''\
# I358:اليونان تحيي أمل التأهل وتقلص فرصة "نسور"ة"
# I357:مظاهرات حاشدة ليهود متشددين دفاعاً عن "العنصرية"
# I356:روسيا تنتقد عقوبات أمريكية أوروبية "أحادية" على إيران\
# '''
# 
# 	print uni2hex(s3)
# 	print uni2uhex(u3)
# 	
# 	return
	# # create dict by hand
	# structure = OrderedDict()
	# structure['one'] = 'Eins'
	# structure['two'] = 'Zwei'
	# structure['three'] = 'Drei'
	# structure['four'] = [True, 2, '3-2', 42.23]
	# 
	# domnode = serialize(structure, nodename='root')
	# print domnode.toprettyxml()
	# 
	# structure2 = deserialize(domnode)
	# print structure2

	# # create dict from XML string
	# node = parseString(s).childNodes[0]
	# print node.toprettyxml()
	# 
	# structure = deserialize(node)
	# print structure
	
	# return
	
	# #slider
	# <to>+38641357777</to>
	# #tantadruj
	# <to>+38631633834</to>
	# #robi
	# <to>+38641992549</to>
	
	hdrs = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	
	# msg = {
	# 	'data': '''
	# 	<clickAPI>
	# 	<sendMsg>
	# 	<api_id>3243293</api_id>
	# 	<user>mmatcher</user>
	# 	<password>mmatcher15</password>
	# 	<to>+38641357777</to>
	# 	<text>''' + HELP +
	# 	'''</text>
	# 	<from>slider</from>
	# 	</sendMsg>
	# 	</clickAPI>
	# 	'''
	# }
	# 
	# conn = HTTPConnection('api.clickatell.com')
	# conn.request('POST', '/xml/xml', urlencode(msg), hdrs)
	# res = conn.getresponse()
	# data = res.read()
	# print data
	# conn.close()
	
	
	# for x in range(70,370):
	# 	s = ''.join(random.choice(string.printable) for z in range(random.randrange(1,70)))
	# 	msg = {
	# 		'text': 'D%d' % x,
	# 		'credentials': 'rgr@mmatcher.com:rgr'
	# 	}
	# 
	# 	conn = HTTPConnection('sms.mmatcher.com')
	# 	conn.request('POST', '/', urlencode(msg), hdrs)
	# 	res = conn.getresponse()
	# 	data = res.read()
	# 	print data
	# 	conn.close()
	
	from mmodules.xmlpolymerase.serializer import serialize
	
	xml = {
		'sendMsg': {
			'api_id': '3243293',
			'user': 'mmatcher',
			'password': 'mmatcher15',
			'to': '38641357777',
			'from': '447624803759',
			# 'text': sms.encode(),
			# 'text': uni2uhex(sms),
			# 'unicode': '1',
			'text': 'test message',
			# 'concat': '5',
			'mo': '1',
			'callback': '3',
		},
	}
	
	dom = serialize(xml, nodename='clickAPI')
	# print dom.toprettyxml()
	# return
	# return dom.toxml('UTF-8')
	
	from httplib import HTTPConnection
	from urllib import urlencode
	
	hdrs = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	msg = {
		'data': dom.toxml('UTF-8'),
	}
	# print '-'*20, urlencode(msg)
	
	conn = HTTPConnection('api.clickatell.com')
	conn.request('POST', '/xml/xml', urlencode(msg), hdrs)
	res = conn.getresponse()
	data = res.read()
	conn.close()
	print data
	return data
	
	
	
	msg = {
		'text': 'I',
		'credentials': 'rgr@mmatcher.com:rgr'
	}
	
	conn = HTTPConnection('sms.mmatcher.com')
	conn.request('POST', '/web', urlencode(msg), hdrs)
	res = conn.getresponse()
	data = res.read()
	print data
	conn.close()
	
	
	# print textToRequest('I')
	# print textToRequest('A selling samsung 19" LCD display')
	# textToRequest('I71')
	# textToRequest('D70')
	# textToRequest('M17:I have 1 for you!')

if __name__ == '__main__':
	main()