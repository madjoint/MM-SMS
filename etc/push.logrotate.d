/var/log/push/*.log {
	daily
	rotate 60
	compress
	missingok
	notifempty
	sharedscripts
	postrotate
		/etc/init.d/push restart
	endscript
}
