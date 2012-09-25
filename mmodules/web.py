from mmodules import rest

#HELP1 = [
#	'SELL/BUY<space>your item=place ad to sell or buy',
#	'C<space> city= your location',
#	'AD = list of placed ads',
#	'AD<ad no.> = list matches for ad <ad no.>',
#	'D<ad no.> = delete ad<ad no.>',
#	'OFF<space>SUB= Unsubscribe',
#]

HELP1 = [
	'To place ad to sell: SELL <space>ad',
	'To place ad to buy: BUY <space>ad',
	'To update Location: C <Space> city',
	'For list of placed ads: AD',
	'For a list of matches ad: AD<ad no.>',
	'To delete ad: D<ad no.>',
	'To unsubscribe: OFF<space>SUB',
	'Send your request as an SMS to 289.',
]


HELP2 = [
	# ('A3 buy dog', 'add: buy dog (valid 3 days)'),
	#('AD', 'List of items'), #interests   #L
	# ('IP2', 'intrsts (pg 2)'),
	#('AD2', 'List matches for item 2'), #interest #L2
	# ('I1P2', 'mtchs for I1 (pg 2)'),
	#('D3', 'Delete item 3'),
	#('OFF SUB', 'Unsubscribe'),
	# ('R3', 'renew I3'),
]


def HTMLhelp():
	return '<pre>\n' + ''.join(['%s\n' % x for x in HELP1]+['%-2s = %s\n' % x for x in HELP2]).replace('<', '&lt;').replace('>', '&gt;') + '</pre>'


def help():
	return ''.join(['%s\n' % x for x in HELP1]+['%s = %s\n' % x for x in HELP2])


def product(op):
	if op == 'zong':
		return 'EZ Trader'
	elif op == 'warid':
		return 'Warid Tijarat'
	return 'mmatcher'


def parse(txt):
	"""Parse SMS message into 3 parameters: cmd, id and msg"""
	import re

	txt = re.sub(r'(\s|<[sS][pP][aA][cC][eE]>)+', ' ', txt.strip().strip("'"))
	
	#when user given ad with L it will convert to Z command to block L or I from SMS
	if re.match(r'^[iIlL](\d)*$', txt.lower()):
		txt = txt.lower().replace('i','z')
		txt = txt.lower().replace('l','z')

	#when user given ad it with AD will convert to L command
	if re.match(r'^(ad)(\d)*$', txt.lower()):
		txt = txt.lower().replace('ad','L')
	
	m = re.match(r'^[iIlL]\s?(\d+)\s?[mM]\s?(\d+)[:\s]+(.+)$', txt) # 'i1m2 txt'
	if m:
		cmd, id, txt =  'M', (m.group(1), m.group(2)), m.group(3)
	else:
		m = re.match(r'^[iIlL]\s?(\d*)\s?[pP]\s?(\d+)[:\s]*$', txt) # 'i1p2' | 'ip2'
		if m:
			cmd, id, txt =  'P', (m.group(1), m.group(2)), ''
		else:

			m = re.match(r'^[aA]\s?(\d+)[:\s]+(.+)$', txt) # 'a3 txt'
			if m:
				cmd, id, txt =  'A', m.group(1), m.group(2)
			else:

				m = re.match(r'^[cC][:\s]+(.+)$', txt) # 'c txt'
				if m:
					cmd, id, txt =  'C', '', m.group(1)
				else:

					m = re.match(r'^([iIlLrRdD])\s?(\d+):?$', txt) # 'i3' | 'r3' | 'd3'
					if m:
						cmd, id, txt =  m.group(1).upper(), m.group(2), ''
					else:

						m = re.match(r'^([iIlLrRhH]):?$', txt) # 'i' | 'r' | 'h' | 's' | 'u'
						if m:
							cmd, id, txt =  m.group(1).upper(), '', ''
						else:

							m = re.match(r'^[iIlL]\s?(\d+)\s?[mM]\s?(\d+)\s?#:?$', txt) # 'i1m2#'	
							
							if m:
								cmd, id, txt =  'X', (m.group(1), m.group(2)), ''
							else:

								m = re.match(r'^sub[:\s]?(free|sim|gol|bus).*$', txt.lower()) # 'sub free, sim, gol, bus'
								if m:
									cmd, id, txt =  'S', m.group(1), ''
								else:

									if re.match(r'^[mM]\s?#:?$', txt): # 'm#'
										cmd, id, txt =  'X', '', ''
									elif re.match(r'^(\?|help)[:\s]?$', txt.lower()): # 'help' | '?'
										cmd, id, txt =  'H', '', ''
									elif re.match(r'^unsub.*$', txt.lower()): # 'unsub'
										cmd, id, txt =  'U', '', ''
									else: # 'text'
										if re.match(r'^(sel|buy).*$', txt.lower()) and (len(txt.split()) > 1):	#kazim 300712
											cmd, id =  'A', ''									
										elif (len(txt) < 7) or (len(txt.split()) < 2):
											cmd, id = 'SHORT', ''
										elif (len(txt) >159) or (len(txt.split()) > 159):
											cmd, id = 'LONG', ''
										else:
											cmd, id =  'LONG', ''

	if cmd == 'L':
		cmd = 'I'
	return cmd, id, txt.strip()

def start(txt, usr, op):
	rest.key_value = rest.kv.KeyValue(usr, rest.send)
	sms = ''
	
	for command in txt.split('|'):
		cmd, lid, msg = parse(command)
		try:
			url, params = rest.encode(op, usr, cmd, lid, msg)
		except rest.NoInterestError:
			sms += "There is no ad 'AD{}'.\nYour ads are:\n".format(lid)
			cmd, lid, msg = 'I', '', ''
			url, params = rest.encode(op, usr, cmd, lid, msg)
		except rest.NoMatchError:
			if lid == '':
				sms += 'There is no conversation going on.\nPlease specify a match number.'
			else:
				sms += "There is no match 'AD{}'.\nPlease specify the correct match number.".format(lid[0] + "M" + lid[1])
			break
		except rest.UnknownCommandError:
			auth = rest.checkAuth(usr)
			if auth:
				if auth == '401':
					if op == 'zong':
						#sms = "Welcome to Dialog MyTrader. You can now post any amount of ads for just Rs1+tax a day. Just subscribe to the service by sending SUB to 289. (Conditions Apply).".format(product(op))
						sms = "Welcome to Dialog MyTrader! To subscribe to the service send SUB to 289. ".format(product(op))
					elif op == 'warid':
						sms = "Please subscribe for using {}.\nYou can subscribe by sending SUB to 8225 for weekly, SUB to 8226 for Monthly, SUB to 8227 for Business package.\n".format(product(op))
					else :
						sms = "Please subscribe for using Mmatcher. You can subscribe by sending sub<space>free to this number. Thanks.".format(product(op))
					break
				else:
					if cmd == 'SHORT':
						sms += 'Your sent ad needs more details. To sell, send SELL<space> ad to 289. To buy, send BUY<space> ad to 289. '
						#sms += 'Your sent ad needs more details such as Buy or Sell, product name, model, quality and price to find best results for your ads.\n E.g. Buy Toyota Axio X 2010 5M.'
						break
					elif cmd == 'LONG':
						sms += 'Your message needs to be less than 160 characters in length. To sell an item, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.'
						break
						#sms += 'Please post Buy/Sell ads with less than 160 characters in length. To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.'
					#else:
			sms += "The command was not recognised. To sell, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289. Send H to 289 for help. "
			#sms += "Your sent ad needs more details. To sell, send SELL<space> ad to 289. To buy, send BUY<space> ad to 289. "
			#sms += "Your sent ad needs more details such as Buy or Sell, product name, model, quality and price to find best results for your ads. E.g. Buy Toyota Axio X 2010 5M."
			break
		except rest.NoLocationError:
			sms += "Unknown City!\n To set your location correctly, type 'C<space>city name' and send to 289. e.g. 'C Colombo' Or Dial #289# > MyTrader > Update Location."
			break
		if url:
			body = rest.send(usr, url, params)
			if body:
				if body == '401':
					if op == 'zong':
						sms = "Welcome to Dialog MyTrader! To subscribe to the service send SUB to 289."
						#sms = "Welcome to Dialog MyTrader. You can now post any amount of ads for just Rs1+tax a day. Just subscribe to the service by sending SUB to 289. (Conditions Apply)." % format(product(op))
						#"Welcome to MyTrader! To subscribe to the service send SUB to 289.".format(product(op))
					elif op == 'warid':
						sms = "Please subscribe for using {}.\nYou can subscribe by sending SUB to 8225 for weekly, SUB to 8226 for Monthly, SUB to 8227 for Business package.\n".format(product(op))
					else :
						sms = "Please subscribe for using Mmatcher. You can subscribe by sending sub<space>free to this number. Thanks.".format(product(op))
					break
				else:
					if cmd == 'SHORT':
						sms += 'Your sent ad needs more details. To sell, send SELL<space> ad to 289. To buy, send BUY<space> ad to 289. '
						break
					elif cmd == 'LONG':
						sms += 'Your message needs to be less than 160 characters in length. To sell an item, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.'
						break
						#sms += 'Please post Buy/Sell ads with less than 160 characters in length. To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.'

					sms += rest.decode(product(op), cmd, lid, body) + '\n'
			else:
				sms += 'EMPTY: ' + command + '\n'
		elif cmd == 'H':
			sms += help() + '\n'
		else:
			sms += 'ERROR: ' + command + '\n'
	if sms:
		sms = sms[:-1]
	return sms