#!/usr/bin/python3
# Depend on
# update-notifier-common 
https://packages.ubuntu.com/disco/update-notifier-common
#
from PyQt5.QtCore import QProcess

class update_worker_t():
    def __init__(self):
        self.m_runner = QProcess()
        self.upgrades = 0
        self.security_upgrades = 0
        
    def check_for_updates(self):
        if self.m_runner.state() == QProcess.NotRunning:
            apt_check= "/usr/lib/update-notifier/apt-check"
            #self.m_runner.finished.connect(self.runner_done)
            self.m_runner.start(apt_check)
            self.m_runner.waitForFinished()
             
            if (self.m_runner.exitStatus() == QProcess.NormalExit and 
self.m_runner.exitCode() == 0):
                result = self.m_runner.readAllStandardError()
                parts = result.trimmed().split(";")
                try:
                    self.upgrades = int(parts[0])
                    self.security_upgrades = int(parts[1])
                except:
                    print ("PARSING OUTPUT FAILED")
                    return
            else:
                print("exit status: " + str (self.m_runner.exitStatus()))
                print("error code: " + str(self.m_runner.exitCode()))
    
        else:
            print ("ALREADY RUNNING")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u",
                      "--upgrader-sw",
                      dest="upg_path",
                      help="Define software/app to open for upgrade",
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
