#!/bin/sh
sudo apt dist-upgrade
echo Upgrade Ended
read -p "Press enter to continue"
sleep 10
read -n 1 -s -r -p "Press any key to continue" variable;echo
