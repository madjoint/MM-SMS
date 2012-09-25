#!/usr/bin/env python3

from datetime import datetime
from time import sleep
import json
from mmodules import rest
from mmodules import smsc
from mmodules import apns

def decode_queue(data):
	queue = []
	data = json.loads(data)
	# print(json.dumps(data, indent=4))
	if data and 'status' in data and data['status'] == 'OK' and 'response' in data and data['response']:
		for user_id, notify_data in data['response'].items():
			if 'info' in notify_data and 'user_data' in notify_data['info'] and notify_data['info']['user_data']:
				if 'apple_push_token' in notify_data['info']['user_data'] and notify_data['info']['user_data']['apple_push_token']:
					notify_method = 'apns'
					notify_uid = notify_data['info']['user_data']['apple_push_token']
				elif 'mobile_number' in notify_data['info']['user_data'] and notify_data['info']['user_data']['mobile_number'] and notify_data['info']['user_data']['operator']:
					notify_method = 'sms'
					notify_uid = notify_data['info']['user_data']['mobile_number']
					notify_op = notify_data['info']['user_data']['operator']
				else:
					return queue
				
				rest.key_value = rest.kv.KeyValue(notify_uid, rest.send)
				rest.key_value.add_manifest(json.dumps(notify_data['info']['manifest']))
				
				if notify_method == 'sms':
					if 'matches' in notify_data:
						interests_data = notify_data['matches']
					else:
						interests_data = notify_data['messages']
					
					for interest_id, interests in interests_data.items():
						if len(interests) == 1:
							if 'matches' in notify_data:
								txt = 'a new match'
							else:
								txt = 'a new message'
						else:
							if 'matches' in notify_data:
								txt = '{} new matches'.format(len(interests))
							else:
								txt = '{} new messages'.format(len(interests))
						
						lo_id = rest.key_value.lo_id(interest_id)
						txt = "Your ad 'AD{}' has {}:\n".format(lo_id, txt)
						for interest in interests:
							mob = interest['mobile_number']
							interest_text = interest['text']
							if interest_text.__len__() > 38:
								interest_text =  interest_text[:38] + '..'
							txt += "{}: {}\n".format(mob[2:], interest_text)
							if not 'matches' in notify_data:
								rest.send('rgr@mmatcher.com', 'get/messages/conversation/' + interest['match_id'], {})
						if len(interests) == 1:
							txt += "\nPls contact for more details. " #\nUse eZ Cash for Payments, dial #111#.
						else:
							txt += "\nPls contact for more details. " #\nUse eZ Cash for Payments, dial #111#.
						
						if 'matches' in notify_data:
							rest.send('rgr@mmatcher.com', 'get/interests/matches/' + interest_id, {})
						
						queue.append({
							'method': notify_method,
							'op': notify_op,
							'uid': notify_uid,
							'msg': txt[:-1],
						})
				elif notify_method == 'apns':
					match_unread = notify_data['info']['manifest']['match_unread']
					msg_unread = notify_data['info']['manifest']['msg_unread']
					
					if match_unread + msg_unread > 0:
						if 'matches' in notify_data:
							interests_data = notify_data['matches']
						else:
							interests_data = notify_data['messages']
					
						for interest_id, interests in interests_data.items():
							if len(interests) == 1:
								if 'matches' in notify_data:
									txt = 'a new match'
								else:
									txt = 'a new message'
							else:
								if 'matches' in notify_data:
									txt = '{} new matches'.format(len(interests))
								else:
									txt = '{} new messages'.format(len(interests))
						
							txt = 'Your interest AD# has {}:\n'.format(txt)
							for interest in interests:
								txt += "AD#: {}\n".format(interest['text'])
					
						queue.append({
							'method': notify_method,
							'op': 'apple',
							'uid': notify_uid,
							'match_unread': match_unread,
							'msg_unread': msg_unread,
							'msg': txt[:-1],
						})
				else:
					print('ERROR: unknown notify_method')
					# print(json.dumps(data, indent=4))
			else:
				print('ERROR: user_data not defined')
				# print(json.dumps(data, indent=4))
	
	return queue


def start(method, number):
	print('[{}]: {}\n'.format(datetime.now(), 'get/queue/' + method + '/' + str(number)))
	
	body = rest.send('rgr@mmatcher.com', 'get/queue/' + method + '/' + str(number), {})
	
	if body:
		queue = decode_queue(body)
	
		for q in queue:
			print('{}[{}]{}: {}'.format(q['method'], q['op'], q['uid'], q['msg']))
			if q['method'] == 'sms':
				smsc.send(q['op'], q['uid'], q['msg'])
			else:
				apns.send(q['uid'], q['match_unread'], q['msg_unread'])


if __name__ == '__main__':
	print('Starting push service...123')
	while True:
		try:
			start('matches', 10)
			# start('messages', 3)
			sleep(1)
		except Exception as e:
			print('Caught exception:', e)
			sleep(1)
