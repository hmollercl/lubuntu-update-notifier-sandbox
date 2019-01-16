#!/usr/bin/python3
# based on apt_check.py
# or
# we could use update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QProgressBar, QTreeView)
from PyQt5 import uic
from PyQt5.QtCore import (Qt, QProcess)
from PyQt5.QtGui import (QStandardItemModel, QIcon)
from optparse import OptionParser
from aptdaemon import client
from aptdaemon.errors import NotAuthorizedError, TransactionFailed
from pathlib import Path

class Dialog(QWidget):
    def __init__(self, options=None):
        QWidget.__init__(self)
        
        self.initUI()
        self.closeBtn.clicked.connect(self.call_reject)
        self.apt_client = client.AptClient()
        self.downloadText = ""
        
        if options.fullUpgrade:
            self.trans2 = self.apt_client.upgrade_system(safe_mode=False)
        else:
            self.trans2 = self.apt_client.upgrade_system(safe_mode=True)
        
        if options.cacheUpdate:
            self.trans1 = self.apt_client.update_cache()
            self.update_cache()
        else:
            self.upgrade()
        
    def initUI(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        self.closeBtn = QPushButton("Close")
        self.progressBar = QProgressBar()
        
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.closeBtn)
        hbox.addStretch(1)
        
        vbox=QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.progressBar)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox) 
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Upgrade')
        self.progressBar.setVisible(False)

    def upgrade_progress(self, transaction, progress):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        #self.label.setText("Applying changes...")
    
    def update_progress(self, transaction, progress):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        self.label.setText("Updating cache...")

    def update_progress_download(self, transaction, uri, status, short_desc, 
                                  total_size, current_size, msg):
        self.downloadText = "Fetching\n" + short_desc
        #self.label.setText(self.detailText + "\n" + self.downloadText)
        self.label.setText(self.downloadText)
    
    def upgrade_progress_download(self, transaction, uri, status, short_desc, 
                                  total_size, current_size, msg):
        self.downloadText = "Downloading " + short_desc
        self.label.setText(self.detailText + "\n" + self.downloadText)
        
    def update_progress_detail(self, transaction, current_items, total_items,
                                current_bytes, total_bytes, current_cps, eta):
        #self.label.setText("Applying changes... " + str(current_items) + " of " + str(total_items))
        if total_items > 0:
            self.detailText = "Fetching " + str(current_items) + " of " + str(total_items)
            self.label.setText(self.detailText + "\n" + self.downloadText)
    
    
    def upgrade_progress_detail(self, transaction, current_items, total_items,
                                current_bytes, total_bytes, current_cps, eta):
        #self.label.setText("Applying changes... " + str(current_items) + " of " + str(total_items))
        if total_items > 0:
            self.detailText = "Downloaded " + str(current_items) + " of " + str(total_items)
            self.label.setText(self.detailText + "\n" + self.downloadText)
    
    def upgrade_finish(self, transaction, exit_state):
        text = "No more Upgrades Available"
        
        reboot_required_path = Path("/var/run/reboot-required")
        if reboot_required_path.exists():
            text = text + "\n" + "Restart required"
        self.progressBar.setVisible(False)
        
        for error in self.errors:
            text = text + "\n" + error
        
        self.label.setText(text)
        self.closeBtn.setVisible(True)
        self.closeBtn.setEnabled(True)

    def upgrade_error(self, transaction, error_code, error_details):
        self.errors.append(error_details)
        self.label.setText(error_details)
        self.closeBtn.setEnabled(True)
        print(error_details)

    def upgrade_cancellable_changed(self, transaction, cancellable):
        self.closeBtn.setEnabled(cancellable)

    def update_cache(self):
        self.closeBtn.setVisible(False)
        self.errors = []
        self.label.setText("Updating cache...")
        try:
            self.trans1.connect('finished', self.update_finish)
            
            self.trans1.connect('progress-changed', self.update_progress)
            self.trans1.connect('progress-details-changed', 
                                     self.update_progress_detail)
            self.trans1.connect('progress-download-changed', 
                                     self.update_progress_download)
            self.trans1.connect('error', self.upgrade_error)
            self.trans1.run()
            #print(self.trans1)
            
        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully:" +
                  "{}".format(e))
    
    def update_finish(self, transaction, exit_state):
        self.label.setText("Update Cache Finished")
        self.upgrade()
        
    def upgrade(self):
        self.errors = []
        self.label.setText("Applying changes...")
        #print(self.apt_client)
        #print(self.trans2)
        try:
            self.trans2.connect('progress-changed', self.upgrade_progress)
            self.trans2.connect('cancellable-changed', 
                                     self.upgrade_cancellable_changed)
            self.trans2.connect('progress-details-changed', 
                                     self.upgrade_progress_detail)
            self.trans2.connect('progress-download-changed', 
                                     self.upgrade_progress_download)
            self.trans2.connect('finished', self.upgrade_finish)
            self.trans2.connect('error', self.upgrade_error)
            self.trans2.run()
            
        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully:" +
                  "{}".format(e))
        
    def call_reject(self):
        app.quit()

class App(QApplication):
    def __init__(self, options, *args):
        QApplication.__init__(self, *args)
        self.dialog = Dialog(options)
        self.dialog.show()


def main(args, options):
    global app
    app = App(options, args)
    app.setWindowIcon(QIcon.fromTheme("system-software-update"))
    app.exec_()


if __name__ == "__main__":
    # check arguments
    parser = OptionParser()
    parser.add_option("",
                      "--cache-update",
                      action="store_true",
                      dest="cacheUpdate",
                      help="Update Cache Before Upgrade")
    parser.add_option("",
                      "--full-upgrade",
                      action="store_true",
                      dest="fullUpgrade",
                      help="Full upgrade same as dist-upgrade")
    (options, args) = parser.parse_args()
    
    #run it
    main(sys.argv, options)
