# !/bin/bash
PATH=/sbin:/bin:/usr/bin
i=0
while [ $i != 7 ]; do 
    echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "Network is Online"
        break;
    else
        echo "Waiting network..."
        sleep 1
    fi
    i=`expr $i + 1`
done


echo "start pulse\n"
who
sleep 5
/usr/bin/pulseaudio -D
sleep 3

echo "start olamiMain\n"
OLAMI_DIR=/home/pi/olami
cd $OLAMI_DIR
/usr/bin/python3 $OLAMI_DIR/olamiMain.py > /var/log/olami.log 2>&1
#/usr/bin/python3 $PWD/olamiMain.py
sleep 100
wait

