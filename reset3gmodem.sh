#!/bin/bash
#
# Reset modem. After a few days or a couple of hundred reconnects Novatel fimrware dies
# PPP can not see this (connection is still possible), but no data gies through

echo "Stopping wvdial service"
supervisorctl stop pppkeepalive
supervisorctl stop wvdial
sleep 2
echo "Force modem reset"
chat -v \
	TIMEOUT 10 \
	''     '+++ATZ'  \
	'OK' 'AT+CFUN=1,1' \
	'OK' '' \
< /dev/ttyUSB0 > /dev/ttyUSB0
sleep 10
echo "Restarting wvdial service"
supervisorctl start wvdial
sleep 10
supervisorctl start pppkeepalive

