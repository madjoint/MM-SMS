#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/mmatcher/sms/bin/pyd
PYTHON=/usr/bin/python3
NAME=manifest
CMD=/mmatcher/sms/$NAME.py
PIDFILE=/var/run/$NAME.pid
LOGDIR=/var/log/$NAME
LOGFILE=$LOGDIR/$NAME.log
USER=deploy

test -x $DAEMON || exit 0

set -e

case "$1" in
  start)
	echo -n "Starting $NAME: "
	touch $PIDFILE
	mkdir -p $LOGDIR
	chown -R $USER:$USER $PIDFILE $LOGDIR
	if start-stop-daemon --start --umask 007 --pidfile $PIDFILE --chuid $USER:$USER --exec $DAEMON -- $CMD $NAME
	then
		echo "started."
	else
		echo "failed."
	fi
	;;
  stop)
	echo -n "Stopping $NAME: "
	if start-stop-daemon --stop --retry 10 --quiet --pidfile $PIDFILE --exec $PYTHON
	then
		echo "stopped."
	else
		echo "failed."
	fi
	rm -f $PIDFILE
	;;

  restart|force-reload)
	${0} stop
	${0} start
	;;
  *)
	echo "Usage: /etc/init.d/$NAME {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
