# !/bin/bash
PATH=/sbin:/bin:/usr/bin

echo "start pulse\n"
who
sleep 5
/usr/bin/pulseaudio -D
sleep 3

echo "start olamiMain\n"
OLAMI_DIR=/home/pi/olami
cd $OLAMI_DIR
#/usr/bin/python3 $OLAMI_DIR/olamiMain.py > /var/log/olami.log 2>&1
/usr/bin/python3 $OLAMI_DIR/olamiMain.py
sleep 100
wait

