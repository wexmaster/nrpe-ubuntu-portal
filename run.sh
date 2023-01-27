#!/bin/bash
set -e
trap "echo SIGNAL" HUP INT QUIT KILL TERM

/etc/init.d/memcached start
/etc/init.d/nagios-nrpe-server start
tail -f /var/log/nrpe.log
