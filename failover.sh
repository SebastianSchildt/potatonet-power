#!/bin/bash


TEST_IP=193.99.144.80
MAIL_ALERT="potato@ibr.cs.tu-bs.de"

ping -I eth0.10 -q -c 5 -w 12 $TEST_IP > /dev/null  && ETH0UP=1 || ETH0UP=0;

ping -I ppp0 -q -c 5 -w 12  $TEST_IP > /dev/null  && PPP0UP=2 || PPP0UP=0;

STATE=$(($ETH0UP + $PPP0UP))

mailtxt=$(date)

r=$(ip rule show  | grep "from all lookup cellular" | wc -l)
if [ "$r" -eq "1" ]
then
	NOW="ppp"
else
	NOW="eth"
fi


echo "Currently $NOW is active"
mailtxt="$mailtxt ACTIVE: $NOW."
echo -n "Current state is: "


case "$STATE" in
  0   ) echo "BOTH broken"
	mailtxt="$mailtxt STATE: BOTH broken."
        CHOICE="eth"
        ;;
  1   ) echo "ETH fine, PPP broken"
	mailtxt="$mailtxt STATE: ETH fine, PPP broken."
        CHOICE="eth"
        ;;
  2   ) echo "ETH broken, PPP fine"
	mailtxt="$mailtxt STATE: ETH broken, PPP fine.."
        CHOICE="ppp"
       ;;
  3   ) echo "BOTH fine"
	mailtxt="$mailtxt STATE: BOTH fine."
        CHOICE="eth"
        ;;
  *   ) echo "Universe broken"
	mailtxt="$mailtxt STATE: Universe broken."
	CHOICE="eth"
       ;;
esac     


if [ "$NOW" != "$CHOICE" ] 
then
	echo "Switching from $NOW to $CHOICE."
	mailtxt="$mailtxt ACTION: Switching from  $NOW to $CHOICE."
	if [ "$CHOICE" == "ppp" ]
	then
		ip rule add from all table cellular
		echo "Disabling Internet for field nodes"
		mailtxt="$mailtxt\nDisabling Internet for field nodes."
		sysctl -w net.ipv4.ip_forward=0
	else
		ip rule del from all table cellular
		echo "Reenabling Internet for field nodes"
		mailtxt="$mailtxt\nReenabling Internet for field nodes."
		sysctl -w net.ipv4.ip_forward=1
	fi
	killall -USR1 autossh
	echo $mailtxt | mail -s "Hotpotato failover" "$MAIL_ALERT"
else
	echo "No action taken"
	mailtxt="$mailtxt ACTION: No action."
fi

