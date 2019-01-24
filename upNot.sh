#!/bin/sh
while true;
    do
        /usr/lib/update-notifier/lubuntu/notifier.py -u ./upgrader.py >> /home/hmoller/update_notifier.log 2>&1
        sleep 60
done;
