#!/bin/sh
while true;
    do
        OUT=`/usr/lib/update-notifier/apt-check 2>&1`
        echo $OUT
        oldIFS=$IFS
        IFS=';'
        j=0
        for STRING in $OUT; do
            case $j in 
                0)
                    UPG=$STRING;;
                1)
                    SEC=$STRING;;
            esac
             j=`expr $j + 1`
        done
        IFS=$oldIFS
        #cd "$( cd "$( dirname "$0" )" && pwd )"
        #./notifier.py -p ./upgrader.py >> ~/update_notifier.log 2>&1
        #date >> ~/update_notifier.log
        ./notifier_gui.py -u $UPG -s $SEC -p terminal
        sleep 3600
done;
