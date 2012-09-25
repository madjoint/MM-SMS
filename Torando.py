#!/usr/bin/env python3
import tornado.ioloop
import tornado.web

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

def process(get) :
    url = '/zong'
    number = get.get_argument("number")
    text = get.get_argument("text")
    sender = get.get_argument("sender")
    if text != None and sender != None:
        num = number	
        print(num)
        #op = 'zong'
        subtxt = text
        #subtxt =subtxt.replace("'",'')
       # meta_data = get['meta_data']
       # smpp = ''meta_data.split('?')
       # print('smpp - split length' + len(smpp))
        append_to_log('/mmatcher/sms/log/' + url + '.log', sender + ' - ' + text)					
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
        body = web.start(subtxt, sender.replace('+',''), url.replace('/',''))        
        logBody = body                
        filename = datetime.now().strftime('/log/' + url + '_sms_usage-%Y%m%U%d.log')
        append_to_log('/mmatcher/sms' + filename, sender + ' !|! ' + subtxt + ' !|! ' +  logBody + ' !|! '+num)
    else:
            body = 'The command was not recognized. To sell, send SELL<space> your item to 289. To buy, send BUY<space>your item to 289. Send H to 289 for help.'
    print(body)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        process(self)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(4485)
    print('Listening on port 4485')
    tornado.ioloop.IOLoop.instance().start()
