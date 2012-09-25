/var/log/sms/*.log {
	daily
	rotate 60
	compress
	missingok
	notifempty
	sharedscripts
	postrotate
		/etc/init.d/sms restart
	endscript
}
