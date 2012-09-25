/var/log/manifest/*.log {
	daily
	rotate 60
	compress
	missingok
	notifempty
	sharedscripts
	postrotate
		/etc/init.d/manifest restart
	endscript
}
