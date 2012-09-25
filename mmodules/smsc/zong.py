def send(number, sms):
	from http.client import HTTPConnection
	from urllib.parse import urlencode

	msg = {
		'username': 'zong',
		'password': 'zong123',
		'to': number,
		'text': sms,
	}

	# return ''
	conn = HTTPConnection('localhost', 13010)
	conn.request('GET', '/cgi-bin/sendsms?'+urlencode(msg))
	res = conn.getresponse()
	if res.status != 202:
		data = res.read()
		print('Error sending SMS: '+data)
	conn.close()
