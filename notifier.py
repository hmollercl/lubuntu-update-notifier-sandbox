#!/usr/bin/python3
# 

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import (Qt, QProcess)
from PyQt5.QtGui import QIcon

from pathlib import Path

from update_worker import update_worker_t
import subprocess

class Dialog(QWidget):
    def __init__(self, upgrades, security_upgrades, reboot_required):
        QWidget.__init__(self)
        self.upgrades = upgrades
        self.security_upgrades = security_upgrades
        
        self.initUI()
        self.upgradeBtn.clicked.connect(self.call_upgrade)
        self.closeBtn.clicked.connect(self.call_reject)
        
    def initUI(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        self.upgradeBtn = QPushButton("Upgrade")
        self.closeBtn = QPushButton("Close")
        
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.upgradeBtn)
        hbox.addWidget(self.closeBtn)
        hbox.addStretch(1)
        
        vbox=QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox) 
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Update Notifier")
        
        if self.upgrades > 0:
            text = "There are %s upgrades available and %s security updates available" % (self.upgrades, self.security_upgrades)
            
        if reboot_required:
            text = text + "\nReboot is needed"
        self.label.setText(text)

    def call_reject(self):
        app.quit()
    
    def call_upgrade(self):
        upg_path= "./upgrader.py"
        '''
        process = QProcess()
        process.startDetached()
        out = process.start(upg_path)
        print(out)
        process.waitForStarted()
        #app.quit()
        '''
        subprocess.call(upg_path)

class App(QApplication):
    def __init__(self, upgrades, security_upgrades, reboot_required, *args):
        QApplication.__init__(self, *args)
        self.dialog = Dialog(upgrades, security_upgrades, reboot_required)
        self.dialog.show()

def main(args, upgrades, security_upgrades, reboot_required):
    global app
    app = App(upgrades, security_upgrades, reboot_required, args)
    app.setWindowIcon(QIcon.fromTheme("system-software-update"))
    app.exec_()

if __name__ == "__main__":
    worker = update_worker_t()
    worker.check_for_updates()
    
    reboot_required_path = Path("/var/run/reboot-required")
    if reboot_required_path.exists():
        reboot_required = True
    else:
        reboot_required = False
        
    if worker.upgrades > 0 or reboot_required:
        main(sys.argv, worker.upgrades, worker.security_upgrades, reboot_required)
