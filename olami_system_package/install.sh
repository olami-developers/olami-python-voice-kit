#!/bin/bash

echo "install olami as system service... "
sudo cp -f olami /etc/init.d/ 
sudo chmod 755 /etc/init.d/olami
sudo cp -f olami.conf /etc/init/
sudo chmod 644 /etc/init/olami.conf
sudo cp -f run_olami /sbin/
sudo chmod 755 /sbin/run_olami
sudo touch /var/log/olami.log
sudo chmod 666 /var/log/olami.log
sudo systemctl enable olami.service
echo "done"


