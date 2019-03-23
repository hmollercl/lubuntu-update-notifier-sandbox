#!/usr/bin/python3
# Depend on
# update-notifier-common 
# https://packages.ubuntu.com/disco/update-notifier-common
#
from PyQt5.QtCore import QProcess

from optparse import OptionParser
import subprocess
from pathlib import Path

class update_worker_t():
    def __init__(self):
        self.upgrades = 0
        self.security_upgrades = 0
        
    def check_for_updates(self):
        apt_check = "/usr/lib/update-notifier/apt-check"
        #output = subprocess.call(apt_check)
        output = subprocess.check_output(apt_check, stderr=subprocess.STDOUT)
        print(output)
        print(subprocess.STDOUT)
        if (subprocess.STDOUT <= 0):
            parts = output.split(b";")
            try:
                self.upgrades = int(parts[0])
                self.security_upgrades = int(parts[1])
            except:
                print ("PARSING OUTPUT FAILED")
                return
        else:
            print(subprocess.STDOUT)
    
        #else:
        #    print ("ALREADY RUNNING")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u",
                      "--upgrader-sw",
                      dest="upg_path",
                      help="Define software/app to open for upgrade",
                      metavar="APP")
    parser.add_option("-n",
                      "--notifier-gui",
                      dest="not_path",
                      help="Define notifier path",
                      metavar="APP")
    (options, args) = parser.parse_args()
    
    worker = update_worker_t()
    worker.check_for_updates()
    
    reboot_required_path = Path("/var/run/reboot-required")
    if reboot_required_path.exists():
        reboot_required = True
    else:
        reboot_required = False
    
    if worker.upgrades > 0 or reboot_required:
        print("llamar gui" + str(worker.upgrades) + " "+ str(worker.security_upgrades))
