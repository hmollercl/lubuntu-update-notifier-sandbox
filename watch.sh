#!/bin/sh
watch -n 60 /usr/lib/update-notifier/lubuntu/notifier.py -u ./upgrader.py >> /home/hmoller/update_notifier.log 2>&1
