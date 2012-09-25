#!/usr/bin/env python3

import json
import settings
from datetime import datetime
from time import sleep
from mmodules import smsc
from mmodules.redis3 import *


def start(redis):
	data = redis.blpop('queue', 60)
	if data and len(data) > 0:
		data = json.loads(data[1])
		if data and 'to' in data and 'text' in data and 'operator' in data:
			print('[{}]: to: {}[{}] - text: {}\n'.format(datetime.now(), data['to'], data['operator'], data['text']))
			smsc.send(data['operator'], data['to'], data['text'])


if __name__ == '__main__':
	print('Starting dequeue service...')
	redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_API_DB)
	while True:
		try:
			start(redis)
		except Exception as e:
			redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_API_DB)
			print('Caught exception:', e)
		sleep(2)
