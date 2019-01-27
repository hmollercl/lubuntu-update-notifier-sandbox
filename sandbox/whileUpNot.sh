#!/bin/sh
while true;
    do
        case "$(pgrep notifier.py | wc -w)" in
            0)  echo "not running"
                /usr/lib/update-notifier/lubuntu/notifier.py -u ./upgrader.py >> /home/hmoller/update_notifier.log 2>&1
                ;;
            1)  echo "running"
                ;;
        esac
    sleep 60
done;
