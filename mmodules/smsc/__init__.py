from http.client import HTTPConnection
from urllib.parse import urlencode
from mmodules.smsc import warid
from mmodules.smsc import zong
import json

def send(operator, number, message):
	number = number.strip('+')
	if operator == 'zong':
		zong.send('+'+number, message)
	elif operator == 'warid':
		warid.send('+'+number, message)
	else:
		import mmodules.smsc.clickatell
		xml = clickatell.encode(number, message)
		if xml:
			clickatell.send(xml)


def geoencode(city, country):
	msg = {
		'q': city+', '+country,
		'output': 'json',
		'oe': 'utf8',
		'sensor': 'true_or_false',
		'key': 'ABQIAAAAzT63NsNCcpw5Af6mLso2FxSgcUpOcSOIawgl-Zf9E7s32CuX-RQF5sRXdcMDlQa3cpL8L_S63UUpFA',
	}

	conn = HTTPConnection('maps.google.com')
	conn.request('GET', '/maps/geo?'+urlencode(msg))
	res = conn.getresponse()
	data = res.read()
	
	conn.close()
	data = json.loads(data.decode("utf-8"))
	
	lat, lng = 0, 0
	loc_name = city
	if data and 'Status' in data and 'code' in data['Status'] and data['Status']['code'] == 200 and 'Placemark' in data:		
		for p in data['Placemark']:
			if 'AddressDetails' in p and 'Country' in p['AddressDetails'] and 'CountryName' in p['AddressDetails']['Country'] \
			and p['AddressDetails']['Country']['CountryName'].lower() == country and 'Point' in p and 'coordinates' in p['Point']:
				lng = p['Point']['coordinates'][0]
				lat = p['Point']['coordinates'][1]
				break
	return lat, lng,loc_name

def send_token(operator, number):
	from mmodules import redis as kv
	key_value = kv.KeyValue(number, None)
	sent_token = key_value.get_token()

	if not sent_token:
		import random
		token = ''.join(random.sample('0123456789', 6))
		key_value.set_token(token)
		op = 'MyTrader'
		if operator == 'warid':
			op = 'Warid Tijarat'
		send(operator, number, 'Your '+op+' Verification code is: ' +token)
	return 'Sent.'


def verify_token(number, token):
	from mmodules import redis as kv
	key_value = kv.KeyValue(number, None)
	sent_token = key_value.get_token()

	if sent_token == token:
		ret = 'Equal.'
	else:
		ret = 'Not equal.'
	return ret
