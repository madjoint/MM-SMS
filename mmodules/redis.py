from .redis3 import *

import settings

class KeyValue:
	def __init__(self, user, send):
		self.redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_SMS_DB)
		self.user = user
		self.send = send

	def add(self, param, id, lo_id):
		print('redis: +', param + id, lo_id)
		self.redis.set(param + id, lo_id)
		print('redis: +', 'u' + self.user + param + lo_id, id)
		self.redis.set('u' + self.user + param + lo_id, id)

	def add_max(self, id, lo_id):
		print('redis: +', 'max' + id, lo_id)
		self.redis.set('max' + id, lo_id)

	def add_last_matchid(self, id):
		print('redis: +', 'u' + self.user + 'mLAST', id)
		self.redis.set('u' + self.user + 'mLAST', id)

	def add_manifest(self, manifest):
		print('redis: +', 'ui' + self.user, manifest)
		self.redis.set('ui' + self.user, manifest)

	def remove(self, param, id, lo_id):
		print('redis: -', param + id, lo_id)
		self.redis.delete(param + id)
		print('redis: -', 'u' + self.user + param + lo_id, id)
		self.redis.delete('u' + self.user + param + lo_id)
		if param == 'm' and self.redis.get('max' + id):
			print('redis: -', 'max' + id, lo_id)
			self.redis.delete('max' + id)

	def __return_ids_and_lo_ids(self, url, param):
		ids = []
		lo_ids = []
		import json
		data = json.loads(self.send(self.user, url, {}))
		if data and 'status' in data and data['status'] == 'OK' and 'response' in data and data['response']:
			for x in data['response']:
				id = x[param]
				ids.append(id)
				lo = self.redis.get(param[0] + id)
				if lo and id != self.redis.get('u' + self.user + param[0] + lo):
					self.remove(param[0], id, lo)
					lo = None
				lo_ids.append(lo)
		return ids, lo_ids

	def __repopulate(self, slots, ids, lo_ids, param):
		for i in range(len(ids)-1, -1, -1):
			if not lo_ids[i]:
				slo = list(slots)
				for lo in slo:
					slots.remove(lo)
					if lo not in lo_ids:
						self.add(param, ids[i], lo)
						break
		return slots

	def id(self, lo_id):
		return self.redis.get('u' + self.user + 'i' + lo_id)

	def matchid(self, lo_mid):
		return self.redis.get('u' + self.user + 'm' + lo_mid)

	def last_matchid(self):
		return self.redis.get('u' + self.user + 'mLAST')

	def lo_id(self, id):
		lo_id = self.redis.get('i' + id)
		if not lo_id:
			self.__repopulate_lo_ids()
			lo_id = self.redis.get('i' + id)
		return lo_id

	def lo_matchid(self, mid, lo_id):
		lo_mid = self.redis.get('m' + mid)
		if not lo_mid:
			self.__repopulate_lo_mids(lo_id)
			lo_mid = self.redis.get('m' + mid)
		return lo_mid

	def manifest(self):
		return self.redis.get('ui' + self.user)

	def __repopulate_lo_ids(self):
		ids, lo_ids = self.__return_ids_and_lo_ids('get/interests/list/', 'id')

		lo0ids = [int(x) for x in lo_ids if x != None]
		if lo0ids:
			max_id = 1 + int(max(lo0ids)) - len(lo0ids)
		else:
			max_id = 1

		slots = [str(x) for x in range(1, max_id + len(lo_ids))]
		self.__repopulate(slots, ids, lo_ids, 'i')

	def __repopulate_lo_mids(self, lo_id):
		id = self.id(lo_id)
		ids, lo_ids = self.__return_ids_and_lo_ids('get/interests/matches/' + id, 'match_id')

		nn = self.redis.get('max' + id)
		if nn:
			max_id = int(nn.split('M')[1]) + 1
		else:
			max_id = 1

		slots = [lo_id + 'M' + str(x) for x in range(max_id, max_id+len(ids))]
		unused = self.__repopulate(list(slots), ids, lo_ids, 'm')

		used = set(slots) - set(unused)
		if used == set():
			self.add_max(id, max(slots))
		else:
			self.add_max(id, max(used))

	def set_token(self, token):
		print('redis: +', 't' + self.user, token)
		self.redis.set('t' + self.user, token)
		self.redis.expire('t' + self.user, 60)

	def get_token(self):
		return self.redis.get('t' + self.user)
		
	
	def store_long_msg(self,sar_ref_num, msg):
		print('redis: +', 'msisdn' + self.user +sar_ref_num, msg)
		self.redis.set('msisdn' + self.user + sar_ref_num, msg)

	def retreive_long_msg(self,sar_ref_num):
		return self.redis.get('msisdn' + self.user + sar_ref_num)
	
	#def delete_long_msg(self,sar_ref_num):
	#	return self.redis.del('msisdn' + self.user + sar_ref_num)