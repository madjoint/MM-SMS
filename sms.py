#!/usr/bin/env python3

# M matcher.com.
# your mobile - your marketplace.
 
import cgi

from urllib.parse import parse_qs
from mmodules.smsc import clickatell 
from mmodules import smsc
from mmodules import web
from datetime import datetime
from mmodules import redis as kv
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/plain')])
	sar_ref_number = 0
	if 'DOCUMENT_ROOT' not in environ:
		environ['DOCUMENT_ROOT'] = '.'
	if 'CONTENT_LENGTH' in environ and environ['CONTENT_LENGTH'] == '':
		environ['CONTENT_LENGTH'] = '0'
	
	append_to_log(environ['DOCUMENT_ROOT'] + '/log/environ.log', str(environ))
	
	url = environ.get('PATH_INFO', '').lower()
	if url == '/help':
		return [web.HTMLhelp().encode('utf-8')]
	
	body = ''
	length = int(environ.get('CONTENT_LENGTH', '0'))
	if length != 0:
		utf8 = str(environ['wsgi.input'].read(length), encoding='utf-8')
		post = parse_qs(utf8)
		
		append_to_log(environ['DOCUMENT_ROOT'] + '/log/post_params.log', str(post))
		
		if url == '/clickatell':
			if 'data' in post:
				append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', post['data'][0])
				sender, txt, body = clickatell.start(post['data'][0])

				filename = datetime.now().strftime('/log/' + url + '_sms_usage-%Y%m%U%d.log')
				append_to_log(environ['DOCUMENT_ROOT'] + filename, sender + ' !|! ' + txt + ' !|! ' +  body)
			else:
				body = 'Wrong params.'
		
		elif url == '/clickatell_callback':
			if 'data' in post:
				append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', post['data'][0])
			else:
				body = 'Wrong params.'
		
		elif url == '/web':
			if 'text' in post and 'credentials' in post:
				append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', post['credentials'][0] + ' - ' + post['text'][0])
				body = web.start(post['text'][0], post['credentials'][0], 'web')
			else:
				body = 'Wrong params.'
		
		else:
			body = 'Wrong url.'
	else:
		if url == '/zong' or url == '/warid':
			get = parse_qs(environ['QUERY_STRING'])
			#concat = ''
			if 'text' in get and 'sender' in get:
				num = get['number'][0]	
				 
				#op = 'zong'
				subtxt = get['text'][0]
				subtxt =subtxt.replace("'",'')
				meta_data = get['meta_data'][0]
				smpp = meta_data.split('?')
				#concat = subtxt
				#sar_params = []
				if (smpp[2] != '') :
					sar_params = smpp[2].split('&')
					if (len(sar_params)>= 3) :
						sar_msg_ref_num = sar_params[0].split('=')[0]
						sar_msg_ref_num_val = sar_params[0].split('=')[1]
						sar_total_segments = sar_params[1].split('=')[0]
						sar_total_segments_val = sar_params[1].split('=')[1]
						sar_segment_seqnum = sar_params[2].split('=')[0]
						sar_segment_seqnum_val = sar_params[2].split('=')[1]
						
						#key_value = kv.KeyValue(get['sender'][0].replace('+',''), None)
						#multipart_msg = ''
						#multipart_msg_ = key_value.retreive_long_msg(sar_msg_ref_num_val)
						#if sar_total_segments_val <= sar_segment_seqnum_val :
						#	if not multipart_msg_:
						#		key_value.store_long_msg(sar_msg_ref_num_val, subtxt)
						#	else :
						#		key_value.store_long_msg(sar_msg_ref_num_val, multipart_msg_ + ' ' + subtxt)
						#else :
						#	multipart_msg = key_value.retreive_long_msg(sar_msg_ref_num_val)
						
						#if sar_segment_seqnum_val == sar_total_segments_val :
						#	multipart_msg = key_value.retreive_long_msg(sar_msg_ref_num_val)
						#	multipart_msg = multipart_msg + subtxt						
							#smsc.send(url.replace('/',''),'00923333036853', multipart_msg)
					
					if sar_segment_seqnum_val == sar_total_segments_val :
						smsc.send(url.replace('/',''),get['sender'][0], 'Your message needs to be less than 160 characters in length. To sell an item, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.')
						#smsc.send(url.replace('/',''),get['sender'][0], 'Please post Buy/Sell ads with less than 160 characters in length. To sell an item: send SELL<space> your item to 289. To buy, send BUY<space>your item to 289.')
				else :	 
					append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', get['sender'][0] + ' - ' + get['text'][0])					
					if url == '/warid' :					
						if num == '8225' :
							subtxt = get['text'][0].lower().replace('sub','sub sim')
						elif num == '8226' :
							subtxt = get['text'][0].lower().replace('sub','sub gol')
						elif num == '8227' :
							subtxt = get['text'][0].lower().replace('sub','sub bus')
						elif num == '8229' :
							subtxt = get['text'][0].lower().replace('sub free','sub')
					elif url == '/zong' :
						print(subtxt)
						subtxt = subtxt.lower()
						#if subtxt == 'sub pa' :
						#	subtxt = subtxt.replace('sub pa','sub sim')
						#elif subtxt == 'sub d' :
						#	subtxt = subtxt.replace('sub d','sub gol')
						#el
						if subtxt == 'sub m' :
							subtxt = subtxt.replace('sub m','sub bus')
						elif subtxt == 'sub off' :
							subtxt = subtxt.replace('sub off','unsub')
						elif subtxt == 'sub free off' :
							subtxt = subtxt.replace('sub free off','unsub')
						elif subtxt == 'off sub' :
							subtxt = subtxt.replace('off sub','unsub')
						elif subtxt == 'sub' :
							subtxt = subtxt.replace('sub','sub bus')
						print(subtxt)
						 
					body = web.start(subtxt, get['sender'][0].replace('+',''), url.replace('/',''))		
					logBody = body
					if url == '/warid':
						smsc.send(url.replace('/',''), get['sender'][0], body)
						body=''
						if subtxt == 'sub sim' or subtxt == 'sub gol' or subtxt == 'sub bus' :
							smsc.send(url.replace('/',''), get['sender'][0], 'Dear User, the Terms of Use for Warid Tijarat are available at http://waridtijarat.waridtel.com Kindly go over the Terms before continuing using this service.')
						
						
					filename = datetime.now().strftime('/log/' + url + '_sms_usage-%Y%m%U%d.log')
					append_to_log(environ['DOCUMENT_ROOT'] + filename, get['sender'][0] + ' !|! ' + subtxt + ' !|! ' +  logBody + ' !|! '+num)
			else:
				body = 'The command was not recognized. To sell, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289. Send H to 289 for help.'
				#body = 'Please resend the ad with more details for us to find the best results for you.' #'Wrong params.4'
		elif url == '/send_token':
			get = parse_qs(environ['QUERY_STRING'])
			if 'sender' in get:
				append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', get['sender'][0] + ' - ' + get['operator'][0])
				
				body = smsc.send_token(get['operator'][0], get['sender'][0].replace('+',''))
			else:
				body = 'Wrong params.'
		elif url == '/verify_token':
			get = parse_qs(environ['QUERY_STRING'])
			if 'sender' in get and 'token' in get:
				append_to_log(environ['DOCUMENT_ROOT'] + '/log/' + url + '.log', get['sender'][0] + ' - ' + get['token'][0])
				body = smsc.verify_token(get['sender'][0].replace('+',''), get['token'][0])

				if body == 'Equal.':
					filename = datetime.now().strftime('/log/web_token-%Y%m%U%d.log')
					append_to_log(environ['DOCUMENT_ROOT'] + filename, get['sender'][0])
			else:
				body = 'Wrong params.'
		else:
			body = 'No params.'

	return [body.encode('utf-8')]


def append_to_log(path, str):
	with open(path, 'a') as f:
		f.write('[{}]: {}\n'.format(datetime.now(), str.replace('\n', ' ')))


if __name__ == '__main__':
	port = 6713
	from wsgiref.simple_server import make_server
	server = make_server('', port, application)
	print('Listening on port {}...'.format(port))
	append_to_log('/mmatcher/sms/log/test.log',"started")
	server.serve_forever()
