#!/usr/bin/env python3

import unittest
import random
import string
import re

from http.client import HTTPConnection
from urllib.parse import urlencode

from mmodules import rest
from mmodules import web
from mmodules import clickatell

class test_1_web_parse(unittest.TestCase):

##########################################################################################

	def test_011_command_m(self):
		self.assertEqual(web.parse('i3m1 text'), ('M', ('3','1'), 'text'))

	def test_012_command_m(self):
		self.assertEqual(web.parse('i3m1:text'), ('M', ('3','1'), 'text'))

	def test_013_command_m(self):
		self.assertEqual(web.parse('i3m1: text'), ('M', ('3','1'), 'text'))

	def test_014_command_m(self):
		self.assertEqual(web.parse('i123m321 text'), ('M', ('123','321'), 'text'))

	def test_015_command_m(self):
		self.assertEqual(web.parse('im1 text'), ('A', '', 'im1 text'))

	def test_016_command_m(self):
		self.assertEqual(web.parse('i3m text'), ('A', '', 'i3m text'))

	def test_017_command_m(self):
		self.assertEqual(web.parse('i3m1text'), ('SHORT', '', 'i3m1text'))

	def test_018_command_m(self):
		self.assertEqual(web.parse('i3m1'), ('SHORT', '', 'i3m1'))

	def test_019_command_m(self):
		self.assertEqual(web.parse('i3m1:'), ('SHORT', '', 'i3m1:'))

	def test_020_command_m(self):
		self.assertEqual(web.parse('i3m1: '), ('SHORT', '', 'i3m1:'))

##########################################################################################

	def test_021_command_p(self):
		self.assertEqual(web.parse('i3p1'), ('P', ('3','1'), ''))

	def test_022_command_p(self):
		self.assertEqual(web.parse('ip1'), ('P', ('','1'), ''))

	def test_023_command_p(self):
		self.assertEqual(web.parse('i3p'), ('SHORT', '', 'i3p'))

	def test_024_command_p(self):
		self.assertEqual(web.parse('ip'), ('SHORT', '', 'ip'))

	def test_025_command_p(self):
		self.assertEqual(web.parse('i3p1:'), ('P', ('3','1'), ''))

	def test_026_command_p(self):
		self.assertEqual(web.parse('i3p1 '), ('P', ('3','1'), ''))

	def test_027_command_p(self):
		self.assertEqual(web.parse('i3p1 text'), ('A', '', 'i3p1 text'))

	def test_028_command_p(self):
		self.assertEqual(web.parse('i3p1:text'), ('SHORT', '', 'i3p1:text'))

	def test_029_command_p(self):
		self.assertEqual(web.parse('i3p1text'), ('SHORT', '', 'i3p1text'))

##########################################################################################

	def test_031_command_a(self):
		self.assertEqual(web.parse('a3 text'), ('A', '3', 'text'))

	def test_032_command_a(self):
		self.assertEqual(web.parse('a3:text'), ('A', '3', 'text'))

	def test_033_command_a(self):
		self.assertEqual(web.parse('a3: text'), ('A', '3', 'text'))

	def test_034_command_a(self):
		self.assertEqual(web.parse('a3text'), ('SHORT', '', 'a3text'))

	def test_035_command_a(self):
		self.assertEqual(web.parse('a3'), ('SHORT', '', 'a3'))

	def test_036_command_a(self):
		self.assertEqual(web.parse('a3:'), ('SHORT', '', 'a3:'))

	def test_037_command_a(self):
		self.assertEqual(web.parse('a3: '), ('SHORT', '', 'a3:'))

##########################################################################################

	def test_051_command_m(self):
		self.assertEqual(web.parse('m text'), ('M', '', 'text'))

	def test_052_command_m(self):
		self.assertEqual(web.parse('m:text'), ('M', '', 'text'))

	def test_053_command_m(self):
		self.assertEqual(web.parse('m: text'), ('M', '', 'text'))

	def test_054_command_m(self):
		self.assertEqual(web.parse('mtext'), ('SHORT', '', 'mtext'))

	def test_055_command_m(self):
		self.assertEqual(web.parse('m'), ('SHORT', '', 'm'))

	def test_056_command_m(self):
		self.assertEqual(web.parse('m '), ('SHORT', '', 'm'))

	def test_057_command_m(self):
		self.assertEqual(web.parse('m:'), ('SHORT', '', 'm:'))

	def test_058_command_m(self):
		self.assertEqual(web.parse('m: '), ('SHORT', '', 'm:'))

##########################################################################################

	def test_061_command_i(self):
		self.assertEqual(web.parse('i3'), ('I', '3', ''))

	def test_062_command_i(self):
		self.assertEqual(web.parse('i3 '), ('I', '3', ''))

	def test_063_command_i(self):
		self.assertEqual(web.parse('i3:'), ('I', '3', ''))

	def test_064_command_i(self):
		self.assertEqual(web.parse('i3: '), ('I', '3', ''))

	def test_065_command_i(self):
		self.assertEqual(web.parse('i3 text'), ('A', '', 'i3 text'))

	def test_066_command_i(self):
		self.assertEqual(web.parse('i3:text'), ('SHORT', '', 'i3:text'))

	def test_067_command_i(self):
		self.assertEqual(web.parse('i3: text'), ('A', '', 'i3: text'))

	def test_068_command_i(self):
		self.assertEqual(web.parse('i3text'), ('SHORT', '', 'i3text'))

##########################################################################################

	def test_071_command_r(self):
		self.assertEqual(web.parse('r3'), ('R', '3', ''))

	def test_072_command_r(self):
		self.assertEqual(web.parse('r3 '), ('R', '3', ''))

	def test_073_command_r(self):
		self.assertEqual(web.parse('r3:'), ('R', '3', ''))

	def test_074_command_r(self):
		self.assertEqual(web.parse('r3: '), ('R', '3', ''))

	def test_075_command_r(self):
		self.assertEqual(web.parse('r3 text'), ('A', '', 'r3 text'))

	def test_076_command_r(self):
		self.assertEqual(web.parse('r3:text'), ('SHORT', '', 'r3:text'))

	def test_077_command_r(self):
		self.assertEqual(web.parse('r3: text'), ('A', '', 'r3: text'))

	def test_078_command_r(self):
		self.assertEqual(web.parse('r3text'), ('SHORT', '', 'r3text'))

##########################################################################################

	def test_081_command_d(self):
		self.assertEqual(web.parse('d3'), ('D', '3', ''))

	def test_082_command_d(self):
		self.assertEqual(web.parse('d3 '), ('D', '3', ''))

	def test_083_command_d(self):
		self.assertEqual(web.parse('d3:'), ('D', '3', ''))

	def test_084_command_d(self):
		self.assertEqual(web.parse('d3: '), ('D', '3', ''))

	def test_085_command_d(self):
		self.assertEqual(web.parse('d3 text'), ('A', '', 'd3 text'))

	def test_086_command_d(self):
		self.assertEqual(web.parse('d3:text'), ('SHORT', '', 'd3:text'))

	def test_087_command_d(self):
		self.assertEqual(web.parse('d3: text'), ('A', '', 'd3: text'))

	def test_088_command_d(self):
		self.assertEqual(web.parse('d3text'), ('SHORT', '', 'd3text'))

##########################################################################################

	def test_091_command_i(self):
		self.assertEqual(web.parse('i'), ('I', '', ''))

	def test_092_command_i(self):
		self.assertEqual(web.parse('i '), ('I', '', ''))

	def test_093_command_i(self):
		self.assertEqual(web.parse('i:'), ('I', '', ''))

	def test_094_command_i(self):
		self.assertEqual(web.parse('i: '), ('I', '', ''))

	def test_095_command_i(self):
		self.assertEqual(web.parse('i text'), ('SHORT', '', 'i text'))

	def test_096_command_i(self):
		self.assertEqual(web.parse('i:text'), ('SHORT', '', 'i:text'))

	def test_097_command_i(self):
		self.assertEqual(web.parse('i: text'), ('A', '', 'i: text'))

	def test_098_command_i(self):
		self.assertEqual(web.parse('itext'), ('SHORT', '', 'itext'))

##########################################################################################

	def test_101_command_r(self):
		self.assertEqual(web.parse('r'), ('R', '', ''))

	def test_102_command_r(self):
		self.assertEqual(web.parse('r '), ('R', '', ''))

	def test_103_command_r(self):
		self.assertEqual(web.parse('r:'), ('R', '', ''))

	def test_104_command_r(self):
		self.assertEqual(web.parse('r: '), ('R', '', ''))

	def test_105_command_r(self):
		self.assertEqual(web.parse('r text'), ('SHORT', '', 'r text'))

	def test_106_command_r(self):
		self.assertEqual(web.parse('r:text'), ('SHORT', '', 'r:text'))

	def test_107_command_r(self):
		self.assertEqual(web.parse('r: text'), ('A', '', 'r: text'))

	def test_108_command_r(self):
		self.assertEqual(web.parse('rtext'), ('SHORT', '', 'rtext'))

##########################################################################################

	def test_111_command_h(self):
		self.assertEqual(web.parse('h'), ('H', '', ''))

	def test_112_command_h(self):
		self.assertEqual(web.parse('h '), ('H', '', ''))

	def test_113_command_h(self):
		self.assertEqual(web.parse('h:'), ('H', '', ''))

	def test_114_command_h(self):
		self.assertEqual(web.parse('h: '), ('H', '', ''))

	def test_115_command_h(self):
		self.assertEqual(web.parse('h text'), ('SHORT', '', 'h text'))

	def test_116_command_h(self):
		self.assertEqual(web.parse('h:text'), ('SHORT', '', 'h:text'))

	def test_117_command_h(self):
		self.assertEqual(web.parse('h: text'), ('A', '', 'h: text'))

	def test_118_command_h(self):
		self.assertEqual(web.parse('htext'), ('SHORT', '', 'htext'))

##########################################################################################

	def test_121_command_s(self):
		self.assertEqual(web.parse('s'), ('S', '', ''))

	def test_122_command_s(self):
		self.assertEqual(web.parse('s '), ('S', '', ''))

	def test_123_command_s(self):
		self.assertEqual(web.parse('s:'), ('S', '', ''))

	def test_124_command_s(self):
		self.assertEqual(web.parse('s: '), ('S', '', ''))

	def test_125_command_s(self):
		self.assertEqual(web.parse('s text'), ('SHORT', '', 's text'))

	def test_126_command_s(self):
		self.assertEqual(web.parse('s:text'), ('SHORT', '', 's:text'))

	def test_127_command_s(self):
		self.assertEqual(web.parse('s: text'), ('A', '', 's: text'))

	def test_128_command_s(self):
		self.assertEqual(web.parse('stext'), ('SHORT', '', 'stext'))

##########################################################################################

	def test_131_command_u(self):
		self.assertEqual(web.parse('u'), ('U', '', ''))

	def test_132_command_u(self):
		self.assertEqual(web.parse('u '), ('U', '', ''))

	def test_133_command_u(self):
		self.assertEqual(web.parse('u:'), ('U', '', ''))

	def test_134_command_u(self):
		self.assertEqual(web.parse('u: '), ('U', '', ''))

	def test_135_command_u(self):
		self.assertEqual(web.parse('u text'), ('SHORT', '', 'u text'))

	def test_136_command_u(self):
		self.assertEqual(web.parse('u:text'), ('SHORT', '', 'u:text'))

	def test_137_command_u(self):
		self.assertEqual(web.parse('u: text'), ('A', '', 'u: text'))

	def test_138_command_u(self):
		self.assertEqual(web.parse('utext'), ('SHORT', '', 'utext'))

##########################################################################################

	def test_141_command_question(self):
		self.assertEqual(web.parse('?'), ('H', '', ''))

	def test_142_command_question(self):
		self.assertEqual(web.parse('? '), ('H', '', ''))

	def test_143_command_question(self):
		self.assertEqual(web.parse('?:'), ('H', '', ''))

	def test_144_command_question(self):
		self.assertEqual(web.parse('?: '), ('H', '', ''))

	def test_145_command_question(self):
		self.assertEqual(web.parse('? text'), ('SHORT', '', '? text'))

	def test_146_command_question(self):
		self.assertEqual(web.parse('?:text'), ('SHORT', '', '?:text'))

	def test_147_command_question(self):
		self.assertEqual(web.parse('?: text'), ('A', '', '?: text'))

	def test_148_command_question(self):
		self.assertEqual(web.parse('?text'), ('SHORT', '', '?text'))

##########################################################################################

	def test_151_command_c(self):
		self.assertEqual(web.parse('m#'), ('C', '', ''))

	def test_152_command_c(self):
		self.assertEqual(web.parse('m# '), ('C', '', ''))

	def test_153_command_c(self):
		self.assertEqual(web.parse('m#:'), ('C', '', ''))

	def test_154_command_c(self):
		self.assertEqual(web.parse('m#: '), ('C', '', ''))

	def test_155_command_c(self):
		self.assertEqual(web.parse('m# text'), ('A', '', 'm# text'))

	def test_156_command_c(self):
		self.assertEqual(web.parse('m#:text'), ('SHORT', '', 'm#:text'))

	def test_157_command_c(self):
		self.assertEqual(web.parse('m#: text'), ('A', '', 'm#: text'))

	def test_158_command_c(self):
		self.assertEqual(web.parse('m#text'), ('SHORT', '', 'm#text'))

##########################################################################################

	def test_161_command_c(self):
		self.assertEqual(web.parse('i3m1#'), ('C', ('3','1'), ''))

	def test_162_command_c(self):
		self.assertEqual(web.parse('i3m1# '), ('C', ('3','1'), ''))

	def test_163_command_c(self):
		self.assertEqual(web.parse('i3m1#:'), ('C', ('3','1'), ''))

	def test_164_command_c(self):
		self.assertEqual(web.parse('i3m1#: '), ('C', ('3','1'), ''))

	def test_165_command_c(self):
		self.assertEqual(web.parse('i3m1# text'), ('A', '', 'i3m1# text'))

	def test_166_command_c(self):
		self.assertEqual(web.parse('i3m1#:text'), ('SHORT', '', 'i3m1#:text'))

	def test_167_command_c(self):
		self.assertEqual(web.parse('i3m1#: text'), ('A', '', 'i3m1#: text'))

	def test_168_command_c(self):
		self.assertEqual(web.parse('i3m1#text'), ('SHORT', '', 'i3m1#text'))

##########################################################################################

	def test_171_command_help(self):
		self.assertEqual(web.parse('help'), ('H', '', ''))

	def test_172_command_help(self):
		self.assertEqual(web.parse('help '), ('H', '', ''))

	def test_173_command_help(self):
		self.assertEqual(web.parse('help:'), ('H', '', ''))

	def test_174_command_help(self):
		self.assertEqual(web.parse('help: '), ('H', '', ''))

	def test_175_command_help(self):
		self.assertEqual(web.parse('help text'), ('A', '', 'help text'))

	def test_176_command_help(self):
		self.assertEqual(web.parse('help:text'), ('SHORT', '', 'help:text'))

	def test_177_command_help(self):
		self.assertEqual(web.parse('help: text'), ('A', '', 'help: text'))

	def test_178_command_help(self):
		self.assertEqual(web.parse('helptext'), ('SHORT', '', 'helptext'))

	def test_179_command_help(self):
		self.assertEqual(web.parse('HELP'), ('H', '', ''))

	def test_180_command_help(self):
		self.assertEqual(web.parse('HeLp'), ('H', '', ''))

##########################################################################################
##########################################################################################

class test_2_rest_encode(unittest.TestCase):
	def test_11_command_a(self):
		self.assertEqual(rest.encode('', 'A', '', ''), ('', {}))

	def test_12_command_a(self):
		self.assertEqual(rest.encode('', 'A', '3', ''), ('', {}))

	def test_13_command_a(self):
		self.assertEqual(rest.encode('', 'A', '', 'message'), ('post/interests/interest', {
				'title': 'message',
				'description': '',
				'distance': '10',
				'expire': 7 * 24,
				'latitude': rest.FAKE_LATITUDE,
				'longitude': rest.FAKE_LONGITUDE,
			}))

	def test_14_command_a(self):
		self.assertEqual(rest.encode('', 'A', '3', 'message'), ('post/interests/interest', {
				'title': 'message',
				'description': '',
				'distance': '10',
				'expire': 3 * 24,
				'latitude': rest.FAKE_LATITUDE,
				'longitude': rest.FAKE_LONGITUDE,
			}))

##########################################################################################

	def test_21_command_i(self):
		self.assertEqual(rest.encode('', 'I', '', ''), ('get/interests/list', {}))

	def test_22_command_i(self):
		self.assertEqual(rest.encode('', 'I', '', 'message'), ('get/interests/list', {}))

	def test_23_command_i(self):
		rest.key_value.add('i', '0001000', '1')
		self.assertEqual(rest.encode('', 'I', '1', ''), ('get/interests/matches/0001000', {}))

	def test_24_command_i(self):
		rest.key_value.add('i', '0002000', '2')
		self.assertEqual(rest.encode('', 'I', '2', 'message'), ('get/interests/matches/0002000', {}))

	def test_25_command_i(self):
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'I', '3', 'message')

	def test_26_command_i(self):
		rest.key_value.remove('i', '0002000', '2')
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'I', '2', 'message')

	def test_27_command_i(self):
		rest.key_value.remove('i', '0001000', '1')
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'I', '1', 'message')

##########################################################################################

	def test_31_command_d(self):
		self.assertEqual(rest.encode('', 'D', '', ''), ('', {}))

	def test_32_command_d(self):
		self.assertEqual(rest.encode('', 'D', '', 'message'), ('', {}))

	def test_33_command_d(self):
		rest.key_value.add('i', '0001000', '1')
		self.assertEqual(rest.encode('', 'D', '1', ''), ('delete/interests/interest/0001000', {}))

	def test_34_command_d(self):
		rest.key_value.add('i', '0002000', '2')
		self.assertEqual(rest.encode('', 'D', '2', 'message'), ('delete/interests/interest/0002000', {}))

	def test_35_command_d(self):
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'D', '3', 'message')

	def test_36_command_d(self):
		rest.key_value.remove('i', '0002000', '2')
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'D', '2', 'message')

	def test_37_command_d(self):
		rest.key_value.remove('i', '0001000', '1')
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'D', '1', 'message')

##########################################################################################

	def test_41_command_m(self):
                self.assertRaises(rest.UnknownCommandError, rest.encode, '', 'M', '', '')

	def test_42_command_m(self):
                self.assertRaises(rest.UnknownCommandError, rest.encode, '', 'M', '1', '')

	def test_43_command_m(self):
                rest.key_value.add('m', '0001000', '3M1')
                self.assertRaises(rest.UnknownCommandError, rest.encode,
                                  '', 'M', ('3','1'), 'message')

	def test_44_command_m(self):
                self.assertRaises(rest.UnknownCommandError, rest.encode,
                                  '', 'M', '', 'message')

	def test_45_command_m(self):
                rest.key_value.add('m', '0002000', '3M2')
                self.assertRaises(rest.UnknownCommandError, rest.encode,
                                  '', 'M', ('3','2'), 'message')

	def test_46_command_m(self):
                self.assertRaises(rest.UnknownCommandError,
                                  rest.encode, '', 'M', '', 'message')

	def test_47_command_m(self):
		with self.assertRaises(rest.UnknownCommandError):
			rest.encode('', 'M', ('3','3'), 'message')

	def test_48_command_m(self):
		rest.key_value.remove('m', '0002000', '3M2')
		with self.assertRaises(rest.UnknownCommandError):
			rest.encode('', 'M', ('3','2'), 'message')

	def test_49_command_m(self):
		rest.key_value.remove('m', '0001000', '3M1')
		with self.assertRaises(rest.UnknownCommandError):
			rest.encode('', 'M', ('3','1'), 'message')

##########################################################################################

	def test_51_command_r(self):
		self.assertEqual(rest.encode('user1', 'R', '', ''), ('post/users/register', {'mobile_number': 'user1'}))

	def test_52_command_r(self):
		self.assertEqual(rest.encode('user2', 'R', '', 'message'), ('post/users/register', {'mobile_number': 'user2'}))

##########################################################################################

	def test_53_command_r(self):
		rest.key_value.add('i', '0003000', '3')
		self.assertEqual(rest.encode('', 'R', '3', ''), ('renew/interests/interest/0003000', {}))

	def test_54_command_r(self):
		self.assertEqual(rest.encode('', 'R', '3', 'message'), ('renew/interests/interest/0003000', {}))

	def test_55_command_r(self):
		rest.key_value.remove('i', '0003000', '3')
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'R', '3', '')

	def test_56_command_r(self):
		with self.assertRaises(rest.NoInterestError):
			rest.encode('', 'R', '3', 'message')

##########################################################################################

	def test_61_command_u(self):
		self.assertEqual(rest.encode('', 'U', '', ''), ('post/users/unregister', {}))

	def test_62_command_u(self):
		self.assertEqual(rest.encode('', 'U', '3', ''), ('post/users/unregister', {}))

	def test_63_command_u(self):
		self.assertEqual(rest.encode('', 'U', '', 'message'), ('post/users/unregister', {}))

	def test_64_command_u(self):
		self.assertEqual(rest.encode('', 'U', '3', 'message'), ('post/users/unregister', {}))

##########################################################################################
##########################################################################################

# class test_3_rest_decode(unittest.TestCase):

##########################################################################################
##########################################################################################

class test_4_clickatell(unittest.TestCase):
	out1 = '<clickAPI><sendMsg><to>'
	out2 = '</to><from>447624803759</from><user>mmatcher</user><unicode>0</unicode><callback>3</callback><concat>5</concat><text>'
	out3 = '</text><mo>1</mo><password>mmatcher15</password><api_id>3243293</api_id></sendMsg></clickAPI>'

	def test_11_encode(self):
			self.assertEqual(clickatell.encode('123', 'message'), self.out1 + '123' + self.out2 + 'message' + self.out3)

	def test_12_encode(self):
			self.assertEqual(clickatell.encode('321', 'message'), self.out1 + '321' + self.out2 + 'message' + self.out3)

	def test_13_encode(self):
			self.assertEqual(clickatell.encode('12345', 'some kind of message'), self.out1 + '12345' + self.out2 + 'some kind of message' + self.out3)

##########################################################################################

	in1 = '<clickmo><api_id>3243293</api_id><moMsgId>554986eb96ba76ede93df0e23a279e34</moMsgId><from>'
	in2 = '</from><to>447624803759</to><timestamp>2010-06-23 14:08:57</timestamp><text>'
	in3 = '</text><charset>ISO-8859-1</charset><udh></udh></clickmo>'

	def test_21_encode(self):
			self.assertEqual(clickatell.decode(self.in1 + '123' + self.in2 + 'message' + self.in3), ('message', '123'))

	def test_22_encode(self):
			self.assertEqual(clickatell.decode(self.in1 + '321' + self.in2 + 'message' + self.in3), ('message', '321'))

	def test_23_encode(self):
			self.assertEqual(clickatell.decode(self.in1 + '12345' + self.in2 + 'some kind of message' + self.in3), ('some kind of message', '12345'))

##########################################################################################
##########################################################################################

class test_5_wsgi_parameters(unittest.TestCase):
	def send(self, path, msg):
		hdrs = {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
		conn = HTTPConnection('localhost:6713')
		conn.request('POST', '/' + path, urlencode(msg), hdrs)
		r = conn.getresponse()
		body = r.read()
		conn.close()
		# print(body)
		return body.decode()

	def test_11_path_root(self):
		self.assertEqual(self.send('', {'data': 'Log this string!'}), 'Wrong url.')

	def test_12_path_root(self):
		self.assertEqual(self.send('', {'text': 'I', 'credentials': 'rgr@mmatcher.com:b87410354627d7f999a52fef67bb608e'}), 'Wrong url.')

##########################################################################################

	def test_21_path_help(self):
		self.assertEqual(self.send('help', ''), web.HTMLhelp())

	def test_22_path_help(self):
		self.assertEqual(self.send('HELP', ''), web.HTMLhelp())

	def test_23_path_help(self):
		self.assertEqual(self.send('HeLp', ''), web.HTMLhelp())

	def test_24_path_help(self):
		self.assertEqual(self.send('HeLP', {'text': 'error string'}), web.HTMLhelp())

	def test_25_path_help(self):
		self.assertEqual(self.send('help/', ''), 'No params.')

##########################################################################################

	def test_31_path_clickatell_cb(self):
		self.assertEqual(self.send('clickatell_callback', ''), 'No params.')

	def test_32_path_clickatell_cb(self):
		self.assertEqual(self.send('clickatell_callback/', ''), 'No params.')

	def test_33_path_clickatell_cb(self):
		self.assertEqual(self.send('clickatell_callback', {'text': 'error string'}), 'Wrong params.')

	def test_34_path_clickatell_cb(self):
		self.assertEqual(self.send('clickatell_callback', {'data': 'Log this string!'}), '')

	def test_35_path_clickatell_cb(self):
		self.assertEqual(self.send('CLICKATELL_CALLBACK', {'data': 'Log this string!'}), '')

	def test_36_path_clickatell_cb(self):
		self.assertEqual(self.send('Clickatell_Callback', {'data': 'Log this string!'}), '')

##########################################################################################

	def test_41_path_web(self):
		self.assertEqual(self.send('web', {'text': 'H', 'credentials': 'rgr@mmatcher.com:b87410354627d7f999a52fef67bb608e'}), web.help())

##########################################################################################

	# def test_path_clickatell(self):
	# 	msg = {
	# 		'data': '''<clickmo>
	# 			<from>38641357777</from>
	# 			<text>i</text>
	# 			</clickmo>''',
	# 	}
	# 	msg2 = {
	# 		'text': 'error string',
	# 	}
	# 	self.assertEqual(self.bulk_tester('clickatell', msg), '')

##########################################################################################
##########################################################################################

class test_6_keyvalue(unittest.TestCase):
	def test_11_id(self):
		self.assertEqual(rest.key_value.id('1'), None)

	def test_12_id(self):
		rest.key_value.add('i', '0001000', '1')
		self.assertEqual(rest.key_value.id('1'), '0001000')

	def test_13_id(self):
		rest.key_value.remove('i', '0001000', '1')
		self.assertEqual(rest.key_value.id('1'), None)

##########################################################################################

	# this test can succed or fail - depends on the previous state of lo_matchid=11 (this is not a real life problem!!!)
	# def test_21_matchid(self):
	# 	self.assertEqual(rest.key_value.matchid('11'), None)

	def test_22_matchid(self):
		rest.key_value.add('m', '0001000', '11')
		self.assertEqual(rest.key_value.matchid('11'), '0001000')

	def test_23_matchid(self):
		rest.key_value.remove('m', '0001000', '11')
		self.assertEqual(rest.key_value.matchid('11'), None)

##########################################################################################

	def test_31_lo_id(self):
		rest.key_value.add('i', '0001000', '2')
		self.assertEqual(rest.key_value.lo_id('0001000'), '2')

	def test_32_lo_id(self):
		rest.key_value.remove('i', '0001000', '2')

##########################################################################################

	def test_41_lo_matchid(self):
		rest.key_value.add('m', '0001000', '21')
		self.assertEqual(rest.key_value.lo_matchid('0001000', 'Not used'), '21')

	def test_42_lo_matchid(self):
		rest.key_value.remove('m', '0001000', '21')

##########################################################################################
##########################################################################################

class test_7_web_workflow(unittest.TestCase):
	def test_011_unregistered(self):
		self.assertEqual(web.start('i', test_user), "mmatcher.com:\nYou have to subscribe for using our service.\nYou can do so by replying 'S' to this number.")

	def test_012_register(self):
		self.assertEqual(web.start('s', test_user), "Thank you for subscribing to mmatcher.com.\nFor instructions on how to use mmatcher reply 'H' to this message.")

	def test_013_register(self):
		self.assertEqual(web.start('r', test_user), "You are already subscribed to mmatcher.com.\nFor instructions on how to use mmatcher reply 'H' to this message.")

##########################################################################################

	def test_021_no_interests(self):
		self.assertEqual(web.start('i', test_user), 'You have no interests. You can add them by sending your interest text.')

	def test_022_add_interest(self):
		self.assertEqual(web.start('onewordtst1', test_user), 'The sent interest is too short. Please, be more specific.')

	def test_023_add_interest(self):
		self.assertEqual(web.start('n tst1', test_user), 'The sent interest is too short. Please, be more specific.')

	def test_024_add_interest(self):
		self.assertEqual(web.start('no tst1', test_user), 'Your interest I1 is added and currently has no matches. Matches will arrive on SMS later.')

	def test_02_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:no tst1')

##########################################################################################

	def test_031_add_interests(self):
		rng = range(2, 15)
		self.assertEqual(web.start(''.join('no tst{}|'.format(x) for x in rng)[:-1], test_user).split('\n'),
						['Your interest I{} is added and currently has no matches. Matches will arrive on SMS later.'.format(x) for x in rng])

	def test_032_list_interests(self):
		self.assertEqual(set(web.start('i', test_user).split('\n')),
						{'I{}:no tst{}'.format(x, x) for x in range(14,0,-1)})

##########################################################################################

	def test_041_delete_interest(self):
		self.assertEqual(web.start('d3|d7', test_user), 'Interest 3 has been deleted.\nInterest 7 has been deleted.')

	def test_042_add_interest(self):
		self.assertEqual(web.start('a12345 tst', test_user), 'Your interest I3 is added with 12345 days validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_043_add_interest(self):
		self.assertEqual(web.start('a0 tst', test_user), 'Your interest I7 is added with 0 days validity. It currently has no matches. Matches will arrive on SMS later.')

##########################################################################################

	def test_051_delete_all_interests(self):
		rng = range(1,15)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_052_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'You have no interests. You can add them by sending your interest text.')

##########################################################################################

	def test_061_add_interest(self):
		self.assertEqual(web.start('a1 buying unittestingtestcases', test_user), 'Your interest I1 is added with 1 day validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_062_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases')

	def test_063_no_matches(self):
		self.assertEqual(web.start('i1', test_user), 'No matches for interest 1.')

	def test_064_no_matches(self):
		self.assertEqual(web.start('i2', test_user), 'There is no interest I2.\nYour interests are:\nI1:buying unittestingtestcases')

##########################################################################################

	def test_071_register2(self):
		self.assertEqual(web.start('s', test_user2), "Thank you for subscribing to mmatcher.com.\nFor instructions on how to use mmatcher reply 'H' to this message.")

	def test_072_list_interests(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

	def test_073_add_interest(self):
		self.assertEqual(web.start('a10 selling unittestingtestcases for 1', test_user2), 'Your interest I1 is added with 10 days validity. It currently has 1 match. More matches will arrive on SMS later.')

	def test_074_list_interests(self):
		self.assertEqual(web.start('i', test_user2), 'I1:selling unittestingtestcases for 1(1)')

	def test_075_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(1)')

	def test_076_list_matches(self):
		self.assertEqual(web.start('i1', test_user2), 'I1M1:buying unittestingtestcases')

	def test_077_list_interests(self):
		self.assertEqual(web.start('i', test_user2), 'I1:selling unittestingtestcases for 1(1)')

	def test_078_send_message(self):
		rest.key_value.mc.delete('u' + test_user2 + 'mLAST')
		self.assertEqual(web.start('m $100?', test_user2), 'The command was not recognised.')

	def test_079_list_interests(self):
		self.assertEqual(web.start('m#', test_user2), 'The command was not recognised.')

	def test_080_send_message(self):
		self.assertEqual(web.start('i1m1 how much?', test_user2), 'The command was not recognised.')

	def test_081_send_message(self):
		self.assertEqual(web.start('m $100?', test_user2), 'The command was not recognised.')

	def test_082_list_interests(self):
		self.assertEqual(web.start('m#', test_user2), 'The command was not recognised.')

	def test_083_send_message(self):
		self.assertEqual(web.start('i1m2 how much?', test_user2), 'The command was not recognised.')

	def test_084_list_interests(self):
		self.assertEqual(web.start('i', test_user2), 'I1:selling unittestingtestcases for 1(1)')

##########################################################################################

	def test_085_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(1)')

	def test_086_add_interests2(self):
		rng = range(2, 10)
		self.assertEqual(web.start(''.join('selling unittestingtestcases for {}|'.format(x) for x in rng)[:-1], test_user2).split('\n'),
						['Your interest I{} is added and currently has 1 match. More matches will arrive on SMS later.'.format(x) for x in rng])

	def test_087_list_interests2(self):
		self.assertEqual(set(web.start('i', test_user2).split('\n')),
						{'I{}:selling unittestingtestcases for {}(1)'.format(x, x) for x in range(9, 0,-1)})

	def test_088_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(9)')

	def test_089_list_matches(self):
		rng = range(1, 10)
		self.assertEqual(set(re.split('[\n:]', web.start('i1', test_user))),
						{'I1M{}'.format(x) for x in rng} | {'selling unittestingtestcases for {}'.format(x) for x in rng})

##########################################################################################

	def test_091_delete_interests2(self):
		rng = [2,4,6,8]
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_092_list_interests2(self):
		self.assertEqual(set(web.start('i', test_user2).split('\n')),
						{'I{}:selling unittestingtestcases for {}(1)'.format(x, x) for x in [9,7,5,3,1]})

	def test_093_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(5)')

	def test_094_list_matches(self):
		rng = [9,7,5,3,1]
		self.assertEqual(set(re.sub(r'I1M\d:', 'I1M?:', web.start('i1', test_user)).split('\n')),
						{'I1M?:selling unittestingtestcases for {}'.format(x) for x in rng})

##########################################################################################

	def test_095_add_interest2(self):
		self.assertEqual(web.start('selling unittestingtestcases for 10', test_user2), 'Your interest I2 is added and currently has 1 match. More matches will arrive on SMS later.')

	def test_096_list_interests2(self):
		self.assertEqual(set(web.start('i', test_user2).split('\n')),
						{'I{}:selling unittestingtestcases for {}(1)'.format(x,y) for x,y in [(9,9),(7,7),(5,5),(3,3),(2,10),(1,1)]})

	def test_097_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(6)')

	def test_098_list_matches(self):
		rng = [10,9,7,5,3,1]
		self.assertEqual(set(re.sub(r'I1M\d0?:', 'I1M?:', web.start('i1', test_user)).split('\n')),
						{'I1M?:selling unittestingtestcases for {}'.format(x) for x in rng})

##########################################################################################

	def test_101_delete_interests2(self):
		rng = [9,7,5,3,2,1]
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_102_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

	def test_103_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases')

	def test_104_list_matches(self):
		self.assertEqual(web.start('i1', test_user), 'No matches for interest 1.')

##########################################################################################

	def test_111_add_interests2(self):
		rng = range(1, 10)
		self.assertEqual(web.start(''.join('selling unittestingtestcases for {}|'.format(x+10) for x in rng)[:-1], test_user2).split('\n'),
						['Your interest I{} is added and currently has 1 match. More matches will arrive on SMS later.'.format(x) for x in rng])

	def test_112_list_interests2(self):
		self.assertEqual(set(web.start('i', test_user2).split('\n')),
						{'I{}:selling unittestingtestcases for {}(1)'.format(x, x+10) for x in range(1, 10)})

	def test_113_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases(9)')

	def test_114_list_matches(self):
		rng = range(11, 20)
		self.assertEqual(set(re.split('[\n:]', web.start('i1', test_user))),
						{'I1M{}'.format(x) for x in rng} | {'selling unittestingtestcases for {}'.format(x) for x in rng})

##########################################################################################

	def test_121_delete_interests2(self):
		rng = range(1, 10)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_122_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

	def test_123_send_message(self):
		self.assertEqual(web.start('i1m1 how much?', test_user2), 'The command was not recognised.')

	def test_124_send_message(self):
		rest.key_value.add('i', '0001000', '1')
		self.assertEqual(web.start('i1', test_user2), 'No matches for interest 1.')

	def test_125_list_interests(self):
		rest.key_value.remove('i', '0001000', '1')
		self.assertEqual(web.start('i', test_user), 'I1:buying unittestingtestcases')

##########################################################################################

	def test_131_add_interest2(self):
		self.assertEqual(web.start('tst tst', test_user2), 'Your interest I1 is added and currently has no matches. Matches will arrive on SMS later.')

	def test_132_add_interest2(self):
		self.assertEqual(web.start('a0 tst', test_user2), 'Your interest I2 is added with 0 days validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_133_add_interest2(self):
		self.assertEqual(web.start('a1 tst', test_user2), 'Your interest I3 is added with 1 day validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_134_add_interest2(self):
		self.assertEqual(web.start('a2 tst', test_user2), 'Your interest I4 is added with 2 days validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_135_add_interest2(self):
		self.assertEqual(web.start('a100 tst', test_user2), 'Your interest I5 is added with 100 days validity. It currently has no matches. Matches will arrive on SMS later.')

	def test_136_delete_interests2(self):
		rng = range(1, 6)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_137_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

##########################################################################################

	def test_141_add_interest2(self):
		self.assertEqual(web.start('selling unittestingtestcases', test_user2), 'Your interest I1 is added and currently has 1 match. More matches will arrive on SMS later.')

	def test_142_add_interest2(self):
		self.assertEqual(web.start('a0 selling unittestingtestcases', test_user2), 'Your interest I2 is added with 0 days validity. It currently has 1 match. More matches will arrive on SMS later.')

	def test_143_add_interest2(self):
		self.assertEqual(web.start('a1 selling unittestingtestcases', test_user2), 'Your interest I3 is added with 1 day validity. It currently has 1 match. More matches will arrive on SMS later.')

	def test_144_add_interest2(self):
		self.assertEqual(web.start('a2 selling unittestingtestcases', test_user2), 'Your interest I4 is added with 2 days validity. It currently has 1 match. More matches will arrive on SMS later.')

	def test_145_add_interest2(self):
		self.assertEqual(web.start('a100 selling unittestingtestcases', test_user2), 'Your interest I5 is added with 100 days validity. It currently has 1 match. More matches will arrive on SMS later.')

	def test_146_delete_interests2(self):
		rng = range(1, 6)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_147_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

##########################################################################################

	def test_151_add_interest(self):
		self.assertEqual(web.start('buying unittestingtestcases', test_user), 'Your interest I2 is added and currently has no matches. Matches will arrive on SMS later.')

	def test_152_add_interest2(self):
		self.assertEqual(web.start('selling unittestingtestcases', test_user2), 'Your interest I1 is added and currently has 2 matches. More matches will arrive on SMS later.')

	def test_153_add_interest2(self):
		self.assertEqual(web.start('a0 selling unittestingtestcases', test_user2), 'Your interest I2 is added with 0 days validity. It currently has 2 matches. More matches will arrive on SMS later.')

	def test_154_add_interest2(self):
		self.assertEqual(web.start('a1 selling unittestingtestcases', test_user2), 'Your interest I3 is added with 1 day validity. It currently has 2 matches. More matches will arrive on SMS later.')

	def test_155_add_interest2(self):
		self.assertEqual(web.start('a2 selling unittestingtestcases', test_user2), 'Your interest I4 is added with 2 days validity. It currently has 2 matches. More matches will arrive on SMS later.')

	def test_156_add_interest2(self):
		self.assertEqual(web.start('a100 selling unittestingtestcases', test_user2), 'Your interest I5 is added with 100 days validity. It currently has 2 matches. More matches will arrive on SMS later.')

	def test_157_delete_interests2(self):
		rng = range(1, 6)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_158_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

##########################################################################################

	def test_161_add_interest(self):
		self.assertEqual(web.start('buying unittestingtestcases', test_user), 'Your interest I3 is added and currently has no matches. Matches will arrive on SMS later.')

	def test_162_add_interest2(self):
		self.assertEqual(web.start('selling unittestingtestcases', test_user2), 'Your interest I1 is added and currently has 3 matches. More matches will arrive on SMS later.')

	def test_163_add_interest2(self):
		self.assertEqual(web.start('a0 selling unittestingtestcases', test_user2), 'Your interest I2 is added with 0 days validity. It currently has 3 matches. More matches will arrive on SMS later.')

	def test_164_add_interest2(self):
		self.assertEqual(web.start('a1 selling unittestingtestcases', test_user2), 'Your interest I3 is added with 1 day validity. It currently has 3 matches. More matches will arrive on SMS later.')

	def test_165_add_interest2(self):
		self.assertEqual(web.start('a2 selling unittestingtestcases', test_user2), 'Your interest I4 is added with 2 days validity. It currently has 3 matches. More matches will arrive on SMS later.')

	def test_166_add_interest2(self):
		self.assertEqual(web.start('a100 selling unittestingtestcases', test_user2), 'Your interest I5 is added with 100 days validity. It currently has 3 matches. More matches will arrive on SMS later.')

	def test_167_delete_interests2(self):
		rng = range(1, 6)
		self.assertEqual(web.start(''.join(['d{}|'.format(x) for x in rng])[:-1], test_user2).split('\n'),
						['Interest {} has been deleted.'.format(x) for x in rng])

	def test_168_list_interests2(self):
		self.assertEqual(web.start('i', test_user2), 'You have no interests. You can add them by sending your interest text.')

##########################################################################################

	def test_171_delete_interest(self):
		self.assertEqual(web.start('d3|d2', test_user), 'Interest 3 has been deleted.\nInterest 2 has been deleted.')

	def test_172_unregister(self):
		self.assertEqual(web.start('u', test_user2), "You are unsubscribed. You can subscribe by replying 'S' to this number. Thank you for using mmatcher.com!")

##########################################################################################

	def test_181_delete_interest(self):
		self.assertEqual(web.start('d2', test_user), 'There is no interest I2.\nYour interests are:\nI1:buying unittestingtestcases')

	def test_182_delete_interest(self):
		self.assertEqual(web.start('d1', test_user), 'Interest 1 has been deleted.')

	def test_183_list_interests(self):
		self.assertEqual(web.start('i', test_user), 'You have no interests. You can add them by sending your interest text.')

	def test_199_unregister(self):
		self.assertEqual(web.start('u', test_user), "You are unsubscribed. You can subscribe by replying 'S' to this number. Thank you for using mmatcher.com!")

##########################################################################################
##########################################################################################

test_user = 'UNIT_TESTER'
test_user2 = 'UNIT_TESTER_2'

if __name__ == '__main__':
	rest.key_value = rest.kv.KeyValue(test_user, rest.send)
	unittest.main()
