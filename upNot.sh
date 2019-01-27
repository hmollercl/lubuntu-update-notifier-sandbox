#!/bin/sh
while true;
    do
        #/usr/lib/update-notifier/lubuntu/notifier.py -p ./upgrader.py >> /home/hmoller/update_notifier.log 2>&1
        cd "$( cd "$( dirname "$0" )" && pwd )"
        ./notifier.py -p ./upgrader.py >> ~/update_notifier.log 2>&1
        date >> ~/update_notifier.log
        sleep 3600
done;
