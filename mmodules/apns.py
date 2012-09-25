from .APNSWrapper import *

def send(token, new_mat, new_msg):
	# create wrapper
	wrapper = APNSNotificationWrapper('mmodules/mmatcher.pem', True)
	
	alert = APNSAlert()
	if new_mat and new_msg:
		alert.loc_key('NewMatchMessageNotify')
	elif new_mat:
		alert.loc_key('NewMatchNotify')
	else:
		alert.loc_key('NewMessageNotify')
	alert.loc_args([new_mat, new_msg])
	
	# create message
	message = APNSNotification()
	message.tokenHex(token)
	message.sound()
	message.badge(new_mat + new_msg)
	message.alert(alert)
	
	# add message to tuple and send it to APNS server
	wrapper.append(message)
	wrapper.notify()
