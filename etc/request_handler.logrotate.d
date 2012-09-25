/var/log/request_handler/*.log {
	daily
	rotate 60
	compress
	missingok
	notifempty
	sharedscripts
	postrotate
		/etc/init.d/request_handler restart
	endscript
}
