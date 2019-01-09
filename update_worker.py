#!/usr/bin/python3
# Depend oon
# update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
from PyQt5.QtCore import QProcess

class update_worker_t():
    def __init__(self):
        self.m_runner = QProcess()
        self.upgrades
        self.security_upgrades
        
    def check_for_updates(self):
        if self.m_runner.state() == QProcess.NotRunning:
            apt_check= "/usr/lib/update-notifier/apt-check"
            #self.m_runner.finished.connect(self.runner_done)
            self.m_runner.start(apt_check)
            self.m_runner.waitForFinished()
             
            if (self.m_runner.exitStatus() == QProcess.NormalExit and self.m_runner.exitCode()==0):
                result = self.m_runner.readAllStandardError()
                parts = result.trimmed().split(";")
                try:
                    self.upgrades = int(parts[0]) #for python list
                except:
                    print ("PARSING OUTPUT FAILED")
                    return
                try:
                    self.security_upgrades = int(parts[1])
                except:
                    #emit error("PARSING OUTPUT FAILED",temporary_failure)
                    print ("PARSING OUTPUT FAILED")
                    return
                #emit updates_available(upgrades,security_upgrades)
                #print ("updates available " + str(self.upgrades) + "," + str(self.security_upgrades))
            #elif m_runner.exitCode()==255:
            #    qDebug() << m_runner->exitStatus() << m_runner->state() << m_runner->error() << m_runner->errorString()
            #    emit error(QString("RUNNER FAILED"),temporary_failure)
            #else:
            #    qDebug() << m_runner->exitStatus() << m_runner->state() << m_runner->error() << m_runner->errorString()
            #    emit error(QString("RUNNER FAILED"),permanent_failure)
            else:
                print(self.m_runner.exitStatus())
                print(self.m_runner.exitCode())
    
        else:
            print ("ALREADY RUNNING")

    def upgrades(self):
        return self.upgrades
    
    def security_upgrades(self):
        return self.security_upgrades
'''    
worker = update_worker_t()
worker.check_for_updates()
print(worker.upgrades)
print(worker.security_upgrades)
'''
