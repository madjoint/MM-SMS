from mmodules import redis as kv

import settings

# # riyadh
# FAKE_LATITUDE = 24.709488
# FAKE_LONGITUDE = 46.675018

# # celje
# FAKE_LATITUDE = 46.23428
# FAKE_LONGITUDE = 15.27683

# none
FAKE_LATITUDE = 0
FAKE_LONGITUDE = 0

ARTICLES = [
	'Selling Suzuki Swift for 700,000 Rs. only',
	'Selling Crate of fresh Oranges for Rs.1000 only',
	'Selling 10marlas Plot in Defence Karachi',
	'Offering English Home tution for Rs.2000/month',
	'Selling Nokia N8 for 25,000 Rs. only',
	'Offering Bridal makeup for 10,000 Rs. only',
	'Selling Ford tractor for 400,000 Rs. only',
	'Buying Washing machine in 20,000 Rs. range',
	'Buying Used Dell laptop for 15,000 Rs.',
	'Need House on rent in Gulberg Colombo',
	'Buying New office furniture',
	'Buying Honda cd 70 bike for 20,000 Rs.',
	'Looking IT job in Islamabad',
	'Buying used LG 32inch LCD',
	'Looking Home tutor for all subjects',
]

class NoInterestError(Exception):
	pass

class NoMatchError(Exception):
	pass

class UnknownCommandError(Exception):
	pass

class NoLocationError(Exception):
	pass

def encode(op, usr, cmd, lid, msg):
	"""Compose REST API url and POST parameters (url, params)"""
	if cmd not in "IACDRUSH":
		raise UnknownCommandError()

	if cmd == 'I':
		if lid == '':
			return 'get/interests/list', {}
		else:
			id = key_value.id(lid)
			if not id:
				raise NoInterestError()
			return 'get/interests/matches/' + id, {}

	if cmd == 'A' and msg != '':
		if not lid:
			lid = '7'
		return 'post/interests/interest', {
			'title': msg,
			'description': '',
			'distance': '500',
			'expire': int(lid) * 24,
			'latitude': FAKE_LATITUDE,
			'longitude': FAKE_LONGITUDE,
		}

	if cmd == 'C' and lid == '' and msg != '':
		from mmodules import smsc

		lat, lng,loc_name = smsc.geoencode(msg, 'sri lanka')
		print(lat)
		print(lng)
		if lat == 0 and lng == 0:
			raise NoLocationError()

		print('lat: {}, long: {}'.format(lat, lng))
		return 'post/users/location', {
			'latitude': lat,
			'longitude': lng,
			'loc_name':loc_name
		}

	if cmd == 'D' and lid != '':
		id = key_value.id(lid)
		if not id:
			raise NoInterestError()
		return 'delete/interests/interest/' + id, {}

	if cmd == 'S' and lid != '':
		expire = 30.5 * 24		
		if lid =='sim':
			expire = 7 * 24
		return 'post/users/register', {
			'mobile_number': usr,
			'operator': op,
			'sub_type': lid,
			'sub_expire': expire,
		}
		

	if cmd == 'R' and lid != '':
		id = key_value.id(lid)
		if not id:
			raise NoInterestError()
		return 'renew/interests/interest/' + id, {}

	if cmd == 'U':
		return 'post/users/unregister', {}

	return '', {}
def checkAuth(usr):
	from http.client import HTTPConnection
	from urllib.parse import urlencode

	hdrs = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Via': 'SMS',
	}
	from base64 import b64encode
	hdrs['Authorization'] = b'Basic ' + b64encode(usr.encode() + b':b87410354627d7f999a52fef67bb608e')
	#print(url, params, hdrs)

	conn = HTTPConnection(settings.API_DOMAIN)
	conn.request('POST', '/' + 'get/interests/list', '', hdrs)
	res = conn.getresponse()
	data = '';
	if res.status == 401:
		data = res.read()
		data = str(data, encoding='utf-8')
		print('Wrong response status:')
		#print(' Command: {}'.format(url))
		print(' Status: {}'.format(res.status))
		print(' Data: {}'.format(data))
		data = '401'
	conn.close()
	return data
def append_to_log(path, str):
	with open(path, 'a') as f:
		f.write('[{}]: {}\n'.format(datetime.now(), str.replace('\n', ' ')))
def send(usr, url, params):
	"""Send request to REST API server and return received data"""
	from http.client import HTTPConnection
	from urllib.parse import urlencode

	hdrs = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Via': 'SMS',
	}

	if url != 'post/users/register':
		from base64 import b64encode
		hdrs['Authorization'] = b'Basic ' + b64encode(usr.encode() + b':b87410354627d7f999a52fef67bb608e')
	print(url, params, hdrs)

	conn = HTTPConnection(settings.API_DOMAIN)
	conn.request('POST', '/' + url, urlencode(params), hdrs)
	res = conn.getresponse()
	if res.status == 200:
		data = res.read()
		data = str(data, encoding='utf-8')
	elif res.status == 401:
		data = res.read()
		data = str(data, encoding='utf-8')
		print('Wrong response status:')
		print(' Command: {}'.format(url))
		print(' Status: {}'.format(res.status))
		print(' Data: {}'.format(data))
		data = '401'
	else:
		data = res.read()
		data = str(data, encoding='utf-8')
		print('Wrong response status:')
		print(' Command: {}'.format(url))
		print(' Status: {}'.format(res.status))
		print(' Data: {}'.format(data))
		data = ''
	conn.close()
	return data


def decode(prod, cmd, lid, data):
	"""Compose SMS message based on cmd and received data"""
	import json

	txt = ''
	data = json.loads(data)
	#print(json.dumps(data, indent=4))
	if data and 'status' in data:
		if data['status'] == 'OK':
			if 'response' in data:
				if cmd == 'I' and lid == '':
					if data['response']:
						lo_ids = []
						for x in data['response']:
							if x['title']:
								lo_ids.append(key_value.lo_id(x['id']))
								if x['match_count']:
									txt += "AD%s: %s(%d)\n" % (lo_ids[-1], x['title'], x['match_count'])
								else:
									txt += "AD%s: %s\n" % (lo_ids[-1], x['title'])
					if txt:
						lo_ids.sort()
						txt += '\nSend '
						for lo_id in lo_ids:
							if lo_id != lo_ids[0]:
								if lo_id == lo_ids[-1]:
									txt += ", "
								else:
									txt += ", "
							txt += "AD%s" % (lo_id)
						txt += ' to see results and mobile numbers of people interested in your selling or buying ads.'
					else:
						from random import choice
						article = choice(ARTICLES)
						if prod == 'EZ Trader':
							txt = "You have not posted any Ads yet. To sell an item, send SELL<space> ad to 289. To buy, send BUY<space> ad to 289. "
							#txt = "You have not posted any ads till now. You can add them by sending sell or buy and your product details to 289. Example : {}".format(article)
						elif prod == 'Warid Tijarat':
							txt = "You have not posted any ads till now. You can add them by sending sell or buy and your product details to 8229. Example : {}".format(article)
						else :
							txt = "You have not posted any Ads yet. To sell an item, send SELL<space> ad to 289. To buy, send BUY<space> ad to 289. "
							#txt = "You have not posted any ads till now. You can add them by sending sell or buy and your product details to this number. Example : {}".format(article)
				elif cmd == 'I' and lid != '':
					if data['response']:
						txt += "Below matches are found for your AD%s\n" % str(lid)
						for x in data['response']:
							if x['title']:
								mob = x['mobile_number']
								txt += "%s: %s\n" % (mob[2:], x['title'])#x['mobile_number']
					if txt:
						if len(data['response']) == 1:
							txt += "\nPls contact for more details. " #Send SMS or call this person's number for more details.
						else:
							txt += "\nPls contact for more details. " #\nUse eZ Cash for Payments, dial #111#.
					else:
						txt = 'No results found for your Ad at the moment. We will notify you as soon as we find a match for your Ad.'

				elif cmd == 'A':
					matches = None
					interest_id = data['response']
					body = json.loads(send('rgr@mmatcher.com', 'get/interests/matches/%s' % interest_id, {}))
					if body and 'status' in body and body['status'] == 'OK' and 'response' in body:
						match_count = len(body['response'])
						if match_count == 1:
							matches = '1 match'
						elif match_count > 1:
							matches = '%s matches' % match_count

					if lid == '':
						validity = ''
					elif lid == '1':
						validity = 'with 1 day validity '
					else:
						validity = 'with %s days validity ' % lid
						
					#print('validity' + validity)
					#print('matches' + matches)
					if matches:
						if prod =='EZ Trader':
							#txt = "Your ad is successfully posted %s and currently has %s. To view the matching ads send 'AD%s' to 289."% (validity, matches, key_value.lo_id(str(interest_id)))
							txt = "Thank you for using My Trader. Your ad has been received and your ad no. is 'AD%s'. It currently has %s . To view the matching ads send 'AD%s' to 289." % (key_value.lo_id(str(interest_id)), matches, key_value.lo_id(str(interest_id)))
						elif prod == 'Warid Tijarat':
							txt = "Your ad is successfully posted %s and currently has %s results. To check results send 'L%s' to 8229 or you can post more ads." % (validity, matches, key_value.lo_id(str(interest_id)))
						else :
							txt = "Thank you for using My Trader. Your ad has been received and your ad no. is 'AD%s'. It currently has %s . To view the matching ads send 'AD%s' to 289." % (key_value.lo_id(str(interest_id)), matches, key_value.lo_id(str(interest_id)))
							#txt = "Your ad is successfully posted and currently has %s matches. To check results send 'AD%s' to 289 or you can post more ads." % (matches, key_value.lo_id(str(interest_id)))
					else:
						txt = "Thank you for using My Trader. Your ad has been received and your ad no. is 'AD%s'. Await matching alerts!" % (key_value.lo_id(str(interest_id)))
						#txt = "Your ad is successfully posted and currently has no matches. Results will be sent to your Phone as soon as we finds a match. Please post your next ad now."#% (key_value.lo_id(str(interest_id)))
						#"Your ad is successfully posted! Ad number: %s Results will be sent to your mobile as soon as we finds a match. Please post your next ad now."% (key_value.lo_id(str(interest_id)))#(validity, matches, key_value.lo_id(str(interest_id)))

				elif cmd == 'D':
					key_value.remove('i', key_value.id(lid), lid)
					#txt = 'AD%s has been deleted. You can also delete ads by dialing #289#>My Trader>Delete Ads.' % lid
					txt = 'You have successfully deleted AD%s. Thank you for using My Trader!' % lid

				elif cmd == 'R' or cmd == 'S':
					if data['response']:
						apiMsg = data['response'].split(';')[1]
						
					
					if data['status'] == 'ERROR_RETREIVING_LOCATION':
						if prod == 'EZ Trader':
							txt = apiMsg#"You are now subscribed to the MyTrader and can start posting ads!  To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.".format(prod)
						elif prod == 'Warid Tijarat':
							txt = "Welcome to Warid Tijarat. To start using the service please set your location by sending C<space>city name to 8229, e.g. C Colombo. For more Help send H to 8229"#.format(prod)
						else:
							txt = "Welcome to Mmatcher. To start using the service please set your location by replying C<space> city name, e.g. C Colombo or send H for more help to this number"#.format(prod)
					else :
						if data['response'] and data['response'].split(':')[0] == 'LOCATION':
							loc = data['response'].split(':')[1]
						
						if prod == 'EZ Trader':
							txt = apiMsg#"You are now subscribed to the MyTrader and can start posting ads!  To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289".format(loc)
						elif prod == 'Warid Tijarat':
							txt = "Welcome to Warid Tijarat. To start using the service please set your location by sending C<space>city name to 8229, e.g. C Colombo. For more Help send H to 8229"#.format(prod)
						else:
							txt = "Welcome to Mmatcher. To start using the service please set your location by replying C<space> city name, e.g. C Colombo or send H for more help to this number"#.format(prod)	
							
				elif cmd == 'C':
					from random import choice
					article = choice(ARTICLES)
					if prod=='EZ Trader':
						txt = "Thank you for updating the location!  To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.".format(prod, article)
					elif prod == 'Warid Tijarat':
						txt = "Great! You are ready to use Warid Tijarat. Post an ad by sending buy or sell<space>your item to 8229.\nFor help send H to 8229.".format(article)
					else :
						txt = "Great! You are ready to use Mmatcher. Post an ad by sending buy or sell<space>your item to this number. For help send H to this number.".format(article)
				elif cmd == 'U':
					if prod == 'EZ Trader':
						txt = "You are successfully unsubscribed from MyTrader. You can subscribe again at anytime by sending SUB to 289. Thank you for using MyTrader! "
						#txt = "You are successfully unsubscribed from MyTrader. You can subscribe again at anytime by sending SUB to 289 or Dial #289#>MyTrader. Thank you for using MyTrader!"
						#"You are successfully unsubscribed from MyTrader. You can subscribe again at anytime, just type SUB and send to 289 or dialing #289#. Thank you for using MyTrader!".format(prod)
					elif prod == 'Warid Tijarat':
						txt = "You are unsubscribed. You can subscribe again by sending Sub to 8225 weekly or sub to 8226 monthly or sub to 8227 business. Thank you for using Warid Tijarat"
					else :
						txt = "You are unubscribed. Please subscribe again by sending sub<space>free to this number. Thank you for using Mmatcher."
			else:
				print('No response.')
		#edited by Mumtaz - 11/12/2012
		elif data['status'] == 'ERROR_INSUFFICIENT_FUND':
			txt = 'You cannot subscribe to MyTrader due to insufficient balance';
		elif data['status'] == 'ERROR_UPGRADE_SUBSCRIPTION':
			txt = "You have reached your selling limit, you can either delete one of your already posted selling ad or upgrade the subscription."
		# end of edit
		#edited by Mumtaz - 02/08/2012
		elif data['status'] == 'ERROR_INTEREST_ALREADY_EXIST':
			txt = "You have already posted this ad."
			#txt = "You have already sent this ad to us. Please send a different Advertisement."
		# end of edit
		elif data['status'] == 'ERROR_REGISTER_USER_MOBILE_NUMBER_EXISTS':
			#code added by kazim raza 16/07/2012
			package_type = '';
			if data['response']=='sim':
				package_type = 'Per ad'
			elif data['response']=='gol':
				package_type = '1 Day'
			elif data['response']=='bus':
				package_type = 'Monthly'
			else :
				package_type = ''			
			
			if prod =='EZ Trader':
				txt = "You are already subscribed to the %s package of MyTrader. To sell an item: send SELL<space> your ad to 289. To buy, send BUY<space>your ad to 289." % (package_type)
			elif prod == 'Warid Tijarat':
				txt = "You are already subscribed to Warid Tijarat.\nFor instructions on how to use Warid Tijarat reply 'H' to this message." #.format(prod)
			else :
				txt = "You are already subscribed to Mmatcher. For instructions on how to use reply 'H' to this number" #.format(prod)
		elif data['status'] == 'ERROR_LATITUDE_NOT_SET' or data['status'] == 'ERROR_LONGITUDE_NOT_SET':
			txt = "Unknown City!\n To set your location correctly, type 'C<space>city name' and send to 289. e.g. 'C Colombo' Or Dial #289# > MyTrader > Update Location."
		elif data['status'] == 'ERROR': # handle unexisting IDs
			if cmd == 'I' and lid != '':
				txt = 'There are no ads posted under AD{}.\nPlease specify the correct ad number (E.g. AD3). You can also find your ads by dialling #289# > MyTrader>Ad List!'.format(lid)
				#txt = 'There is no ad posted with this number I{}.\nPlease specify the correct posted ad number. For assistance on using this service, reply with H. Thanks!'.format(lid)
			elif data['response'] and data['response'].split(':')[0] == 'MORE_WORDS':
				txt = data['response'].split(':')[1]
			elif data['response'] and data['response'].split(':')[0] == 'FORBIDDEN_WORDS':
				from random import choice
				article = choice(ARTICLES)
				word = data['response'].split(':')[1]
				txt = "The word '%s' is blacklisted. If you continue to use blacklisted words, your number will be blocked." % (word)
			else:
				print(json.dumps(data, indent=4))
				#txt = 'Unknown error.\nPlease verify and resend the correct message to the same number. Thanks!'
				txt = 'We are unable to assist you at the moment. Please try again later.'
		else:
			print(json.dumps(data, indent=4))
			#txt = 'Unknown response.\nPlesae verify and resend the correct message to the same number. Thanks!'
			txt = 'We are unable to assist you at the moment. Please try again later.'
	else:
		txt = 'The command was not recognized. To sell, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289. Send H to 289 for help. '

	return txt 
