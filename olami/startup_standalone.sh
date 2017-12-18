# !/bin/bash
PATH=/sbin:/bin:/usr/bin

PS_OUTPUT=$(ps -ax | grep olamiMain.py | grep python3 | awk '{print $1}')
if [ ! -z $PS_OUTPUT ]; then
    echo "kill background olamiMain.py"
    kill -9 $PS_OUTPUT
fi
PS_OUTPUT=$(ps -ax | grep pulseaudio | grep bin | awk '{print $1}')
if [ ! -z $PS_OUTPUT ]; then
    echo "kill background pulseaudio"
    kill -9 $PS_OUTPUT
fi
sleep 1

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

