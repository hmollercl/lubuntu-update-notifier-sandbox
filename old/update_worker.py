#!/usr/bin/python3
# Depend on
# update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
#from PyQt5.QtCore import QProcess
import subprocess

class update_worker_t():
    def __init__(self):
        #self.m_runner = QProcess()
        self.upgrades = 0
        self.security_upgrades = 0
        self.packages = []

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


    def check_updates_names(self):
        apt_check = "/usr/lib/update-notifier/apt-check"
        #output = subprocess.call(apt_check)
        output = subprocess.check_output([apt_check, '-p'], stderr=subprocess.STDOUT)
        print(output)
        print(subprocess.STDOUT)
        if (subprocess.STDOUT <= 0):
            #parts = output.split(b"\n")
            try:
                #self.packages = int(parts[0])
                self.packages = output.split(b"\n")
                self.upgrades = len(self.packages)
            except:
                print ("PARSING OUTPUT FAILED")
                return
        else:
            print(subprocess.STDOUT)
'''    def check_for_updates(self):
        if self.m_runner.state() == QProcess.NotRunning:
            apt_check= "/usr/lib/update-notifier/apt-check"
            #self.m_runner.finished.connect(self.runner_done)
            self.m_runner.start(apt_check)
            self.m_runner.waitForFinished()

            if (self.m_runner.exitStatus() == QProcess.NormalExit and self.m_runner.exitCode() == 0):
                result = self.m_runner.readAllStandardError()
                print(result)
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
            print ("ALREADY RUNNING")'''
