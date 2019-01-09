#!/usr/bin/python3
# based on apt_check.py
# or
# we could use update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
import sys
import apt
import apt_pkg
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
#from PyQt5 import uic
from PyQt5.QtCore import (Qt, QProcess)
from PyQt5.QtGui import (QStandardItemModel, QIcon)
import os
import time
from optparse import OptionParser
import gettext
import subprocess

from aptdaemon import client
from aptdaemon.errors import NotAuthorizedError, TransactionFailed
from pathlib import Path

from update_worker import update_worker_t

class Dialog(QWidget):
    def __init__(self, upgrades, security_upgrades, reboot_required):
        QWidget.__init__(self)
        #uic.loadUi("designer/update_notifier.ui", self)
        self.upgrades = upgrades
        self.security_upgrades = security_upgrades
        
        self.initUI()
        #self.upgrade_swBtn.clicked.connect(self.call_update_software)
        #self.upgradeBtn.clicked.connect(self.upgrade)
        self.closeBtn.clicked.connect(self.call_reject)
        
    def initUI(self):
        self.label = QLabel()
        #self.upgrade_swBtn
        #self.upgrade_swBtn
        self.closeBtn = QPushButton("Close")
        
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.closeBtn)
        hbox.addStretch(1)
        
        vbox=QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox) 
        self.setGeometry(300, 300, 300, 150)
        
        self.setWindowTitle('Update Notifier')
        
        #self.progressBar.setVisible(False)
        
        if self.upgrades > 0:
            text = "There are %s upgrades available and %s security updates available" % (self.upgrades, self.security_upgrades)
            
        if reboot_required:
            text = text + "\n Reboot is needed"
        self.label.setText(text)

    def call_reject(self):
        app.quit()

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
    
    global reboot_required_path
    reboot_required_path = Path("/var/run/reboot-required")
    if reboot_required_path.exists():
        reboot_required = True
    else:
        reboot_required = False
        
    if worker.upgrades > 0 or reboot_required:
        #main(sys.argv, depcache, cache, upgrades, security_updates)
        main(sys.argv, worker.upgrades, worker.security_upgrades, reboot_required)
    
        
