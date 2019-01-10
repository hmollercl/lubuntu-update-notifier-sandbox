#!/usr/bin/python3
# based on apt_check.py
# or
# we could use update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
import sys
import apt
import apt_pkg
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QProgressBar, QTreeView)
from PyQt5 import uic
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

class Dialog(QWidget):
    def __init__(self, cacheUpdate, fullUpgrade):
        QWidget.__init__(self)
        #uic.loadUi("designer/update_notifier.ui", self)
        #self.upgrades = upgrades
        
        self.initUI()
        #self.upgrade_swBtn.clicked.connect(self.call_update_software)
        self.upgradeBtn.clicked.connect(self.upgrade)
        self.closeBtn.clicked.connect(self.call_reject)
        
    def initUI(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        self.upgradeBtn = QPushButton("Upgrade")
        self.closeBtn = QPushButton("Close")
        self.progressBar = QProgressBar()
        self.treeView = QTreeView()
        
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
        self.setWindowTitle('Upgrade')
        
        
        self.progressBar.setVisible(False)

'''        
        if self.upgrades > 0:
            self.label.setText("There are %s upgrades available and %s security updates available, do you want to Upgrade, open the Update Software or Close? \n The following are the affected packages:" % (upgrades, security_updates))
            #self.label.setText("There are %s upgrades available and %s security updates available, do you want to Update? \n The following are the affected packages:" % (upgrades, security_updates))
            self.model = self.createViewModel(self)
            self.treeView.setModel(self.model)
            self.treeView.setRootIsDecorated(False)
            self.treeView.setAlternatingRowColors(True)
            
            self.install_pkgs = []
            self.remove_pkgs = []
            self.upgrade_pkgs = []
            
            for pkg in cache.packages:
                if depcache.marked_install(pkg):
                    self.model.insertRow(0)
                    self.model.setData(self.model.index(0, 0), "Install")
                    self.model.setData(self.model.index(0, 1), pkg.name)
                    self.install_pkgs.append(pkg.name)
                elif depcache.marked_upgrade(pkg):
                    self.model.insertRow(0)
                    self.model.setData(self.model.index(0, 0), "Upgrade")
                    self.model.setData(self.model.index(0, 1), pkg.name)
                    self.upgrade_pkgs.append(pkg.name)
                elif depcache.marked_delete(pkg):
                    self.model.insertRow(0)
                    self.model.setData(self.model.index(0, 0), "Delete")
                    self.model.setData(self.model.index(0, 1), pkg.name)
                    self.remove_pkgs.append(pkg.name)
            
            self.treeView.setSortingEnabled(True)
            self.treeView.sortByColumn(0,Qt.SortOrder())
            self.treeView.setSortingEnabled(False)

        else:
            self.label.setText("Restart Needed")
            self.upgradeBtn.setVisible(False)
            self.upgrade_swBtn.setVisible(False)
            self.setVisible(False)
'''            
    def upgrade_progress(self, transaction, progress):
        self.upgradeBtn.setVisible(False)
        self.upgrade_swBtn.setVisible(False)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        self.label.setText("Applying changes...")

    
    def upgrade_progress_download(self, transaction, uri, status, short_desc, 
                                  total_size, current_size, msg):
        self.downloadText = "Downloading " + short_desc
        self.label.setText(self.detailText + "\n" + self.downloadText)
        #print("download")
        #print(uri)
        #print(short_desc)
        #print(current_size)
        #print(total_size)
        #print(msg)
        
    
    def upgrade_progress_detail(self, transaction, current_items, total_items,
                                current_bytes, total_bytes, current_cps, eta):
        #self.label.setText("Applying changes... " + str(current_items) + " of " + str(total_items))
        if total_items > 0:
            self.detailText = "Downloaded " + str(current_items) + " of " + str(total_items)
            if self.downloadText in locals():
                self.label.setText(self.detailText + "\n" + self.downloadText)
            else:
                self.label.setText(self.detailText)
        
        #print("detail")
        #print(current_items)
        #print(total_items)
        #print(current_bytes)
        #print(total_bytes)
        #print(current_cps)
        #print(eta)

    def upgrade_finish(self, transaction, exit_state):
        text = "Upgrade Complete"
        if reboot_required_path.exists():
            text = text + "\n" + "Restart required"
        self.progressBar.setVisible(False)
        
        for error in self.errors:
            text = text + "\n" + error
        
        self.label.setText(text)
        self.closeBtn.setVisible(True)
        self.upgradeBtn.setVisible(False)
        self.upgrade_swBtn.setVisible(False)
        self.closeBtn.setEnabled(True)

    def upgrade_error(self, transaction, error_code, error_details):
        self.upgradeBtn.setVisible(False)
        self.upgrade_swBtn.setVisible(False)
        self.errors.append(error_details)
        self.label.setText(error_details)
        self.closeBtn.setEnabled(True)

    def upgrade_cancellable_changed(self, transaction, cancellable):
        self.closeBtn.setEnabled(cancellable)

    def createViewModel(self,parent):
        model = QStandardItemModel(0 , 2, parent)
        model.setHeaderData(0, Qt.Horizontal, "Action")
        model.setHeaderData(1, Qt.Horizontal, "Package")
        return model

    def upgrade(self):
        self.progressBar.setVisible(False)
        self.treeView.setVisible(False)
        self.errors = []
        self.label.setText("Applying changes...")
        
        self.apt_client = client.AptClient()
        try:
            #self.transaction = self.apt_client.commit_packages(install=self.install_pkgs, remove=self.remove_pkgs, reinstall=[], purge=[], upgrade=self.upgrade_pkgs, downgrade=[])
            self.transaction = self.apt_client.upgrade_system(safe_mode=False)
            self.transaction.connect('progress-changed', self.upgrade_progress)
            self.transaction.connect('cancellable-changed', 
                                     self.upgrade_cancellable_changed)
            self.transaction.connect('progress-details-changed', 
                                     self.upgrade_progress_detail)
            self.transaction.connect('progress-download-changed', 
                                     self.upgrade_progress_download)
            self.transaction.connect('finished', self.upgrade_finish)
            self.transaction.connect('error', self.upgrade_error)
            self.transaction.run()
        
        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully:" +
                  "{}".format(e))
        
    def call_reject(self):
        app.quit()

class App(QApplication):
    def __init__(self, cacheUpdate, fullUpgrade *args):
        QApplication.__init__(self, *args)
        self.dialog = Dialog(cacheUpdate, fullUpgrade)
        self.dialog.show()


def main(args, cacheUpdate, fullUpgrade):
    global app
    app = App(cacheUpdate, fullUpgrade, args)
    app.setWindowIcon(QIcon.fromTheme("system-software-update"))
    app.exec_()


if __name__ == "__main__":
	#option to update cache or not
	#option to full-upgrade or safe-upgrade
	cacheUpdate = False
	fullUpgrade = False
	main(sys.argv, cacheUpdate, fullUpgrade)
        
