/var/log/dequeue/*.log {
	daily
	rotate 60
	compress
	missingok
	notifempty
	sharedscripts
	postrotate
		/etc/init.d/dequeue restart
	endscript
}
