XML = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<clickmo>
	<api_id>3243293</api_id>
	<moMsgId>2363036fd9e75cf0289015dd18cbe700</moMsgId>
	<from>38641357777</from>
	<to>447624803759</to>
	<timestamp>2010-06-21 11:36:26</timestamp>
	<text>I</text>
	<charset>ISO-8859-1</charset>
	<udh></udh>
</clickmo>
'''


def toUCS2hex(text):
	ucs2 = ''
	uni = 0
	for x in text:
		e = x.encode('unicode_escape')
		if len(e) != 6:
			ucs2 += hex(ord(x)).lstrip('0x').zfill(4)
		else:
			ucs2 += e[2:].decode()
			uni = 1
	return uni, ucs2


def encode(number, sms):
	from .xmlpolymerase.serializer import serialize
	
	uni, hex = toUCS2hex(sms)
	print('Unicode: {}\n{}'.format(uni, sms))
	if uni:
		sms = hex
	
	source = '61429100713'
	# if number[0:3] == '386':
	# 	source = '447624803759'
	# else:
	# 	source = '41798073036'
	
	xml = {
		'sendMsg': {
			'api_id': '3243293',
			'user': 'mmatcher',
			'password': 'mmatcher15',
			'from': source,
			'to': number,
			'text': sms,
			'unicode': str(uni),
			'callback': '3',
			'concat': '5',
			'mo': '1',
		},
	}
	
	dom = serialize(xml, nodename='clickAPI')
	# print(dom.toprettyxml())
	return dom.toxml('utf-8').decode()


def send(xml):
	from http.client import HTTPConnection
	from urllib.parse import urlencode
	
	hdrs = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	msg = {
		'data': xml,
	}
	
	# return ''
	conn = HTTPConnection('api.clickatell.com')
	conn.request('POST', '/xml/xml', urlencode(msg), hdrs)
	res = conn.getresponse()
	data = res.read()
	conn.close()
	return data


def decode(xml):
	from re import sub
	from xml.dom.minidom import parseString
	from .xmlpolymerase.deserializer import deserialize
	
	# create dict from XML string
	node = parseString(xml).childNodes[0]
	# print node.toprettyxml()
	
	xml = deserialize(node)
	
	return xml['text'], sub(r'[^\d]','', xml['from'])


def start(xml):
	from mmodules import web
	txt, usr = decode(xml)
	sms = web.start(txt, usr, 'clickatell')
	xml = encode(usr, sms)
	if xml:
		out = send(xml)
	return usr, txt, sms

