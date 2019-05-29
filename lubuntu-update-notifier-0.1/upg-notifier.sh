#!/bin/sh
while true;
    do
        OUT=`/usr/lib/update-notifier/apt-check 2>&1`
        #echo $OUT
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
        /usr/lib/python3/dist-packages/lubuntu-update-notifier/notifier.py -u $UPG -s $SEC -p /usr/lib/python3/dist-packages/lubuntu-update-notifier/upgrader.py
        sleep 3600
done;
