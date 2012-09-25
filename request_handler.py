#!/usr/bin/env python3

from datetime import datetime
from time import sleep
import json
import settings
import os
from mmodules import rest
from mmodules import smsc
from mmodules import web
from mmodules import apns
from mmodules.redis3 import *
from threading import Thread
def process(queue) :
    url = '/zong'
    get = json.loads(queue)
    print(get)
    if 'text' in get and 'sender' in get:
        num = get['number']	
        print(num)
        #op = 'zong'
        subtxt = get['text']
        #subtxt =subtxt.replace("'",'')
       # meta_data = get['meta_data']
       # smpp = ''meta_data.split('?')
       # print('smpp - split length' + len(smpp))
        append_to_log('/mmatcher/sms/log/' + url + '.log', get['sender'] + ' - ' + get['text'])					
        print(subtxt)
        subtxt = subtxt.lower()
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
        body = web.start(subtxt, get['sender'].replace('+',''), url.replace('/',''))        
        logBody = body                
        filename = datetime.now().strftime('/log/' + url + '_sms_usage-%Y%m%U%d.log')
        append_to_log('/mmatcher/sms' + filename, get['sender'] + ' !|! ' + subtxt + ' !|! ' +  logBody + ' !|! '+num)
    else:
            body = 'The command was not recognized. To sell, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289. Send H to 289 for help.'
    smsc.send('zong',get['sender'].replace('+',''), body)
    #sleep()
    
def start(redis):
    #print("popping data from Redis")
    queue_data = redis.rpop("req_queue")
    #print(queue_data)
    process(queue_data)
    

def append_to_log(path, str):
	with open(path, 'a') as f:
		f.write('[{}]: {}\n'.format(datetime.now(), str.replace('\n', ' ')))

if __name__ == '__main__':
        print('Starting Queue Handler service...123')
        #print(os.environ['DOCUMENT_ROOT'])
        redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_API_DB)
        while True:
            try:
                start(redis)
                #for i in range(100):
                #    t = Thread(target=start, args=(redis,))
                #    t.start()
                # start('messages', 3)
                #sleep(1)
            except Exception as e:
                #sleep(1)
                continue
