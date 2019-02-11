#!/usr/bin/python3
# deppend on
# -aptdaemon
# -debconf-kde-helper
import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QProgressBar, QTreeView, QTextEdit)
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
        self.detailText = ""

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
        self.textEdit = QTextEdit()

        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.closeBtn)
        hbox.addStretch(1)

        vbox=QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.progressBar)
        vbox.addWidget(self.textEdit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 500, 150)
        self.setWindowTitle('Upgrade')
        self.progressBar.setVisible(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setVisible(False)

    def upgrade_progress(self, transaction, progress):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)

    def update_progress(self, transaction, progress):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        self.label.setText("Updating cache...")

    def update_progress_download(self, transaction, uri, status, short_desc,
                                  total_size, current_size, msg):
        self.textEdit.setVisible(True)
        #self.downloadText = "Fetching\n" + short_desc
        #self.label.setText(self.detailText + "\n" + self.downloadText)
        #self.label.setText(self.downloadText)
        self.textEdit.append(status + " " + short_desc + " " + str(current_size) + "/" + str(total_size) + " " + msg)

    def upgrade_progress_download(self, transaction, uri, status, short_desc,
                                  total_size, current_size, msg):
        self.textEdit.setVisible(True)
        #self.downloadText = "Downloading " + short_desc
        #self.label.setText(self.detailText + "\n" + self.downloadText)
        self.textEdit.append(status + " " + short_desc + " " + str(current_size) + "/" + str(total_size) + " " + msg)

    def update_progress_detail(self, transaction, current_items, total_items,
                                current_bytes, total_bytes, current_cps, eta):
        self.textEdit.setVisible(True)
        #self.label.setText("Applying changes... " + str(current_items) + " of " + str(total_items))
        if total_items > 0:
            self.detailText = "Fetching " + str(current_items) + " of " + str(total_items)
            self.label.setText(self.detailText + "\n" + self.downloadText)


    def upgrade_progress_detail(self, transaction, current_items, total_items,
                                current_bytes, total_bytes, current_cps, eta):
        #self.label.setText("Applying changes... " + str(current_items) + " of " + str(total_items))
        self.textEdit.setVisible(True)
        if total_items > 0:
            if self.detailText != "Downloaded " + str(current_items) + " of " + str(total_items):
                self.detailText = "Downloaded " + str(current_items) + " of " + str(total_items)
                self.label.setText(self.detailText + "\n" + self.downloadText)
                self.textEdit.append(self.detailText + "\n" + self.downloadText)

    def upgrade_finish(self, transaction, exit_state):
        text = "Upgrade finished"

        reboot_required_path = Path("/var/run/reboot-required")
        if reboot_required_path.exists():
            text = text + "\n" + "Restart required"
        self.progressBar.setVisible(False)

        if(len(self.errors)>0):
            text = text + " with some errors:"

        self.label.setText(text)
        self.closeBtn.setVisible(True)
        self.closeBtn.setEnabled(True)

    def upgrade_error(self, transaction, error_code, error_details):
        self.textEdit.setVisible(True)
        self.errors.append("Eror Code: " + str(error_code) + "\n")
        self.errors.append("Error Detail: " + error_details + "\n")
        for error in self.errors:
            self.textEdit.append(error)
        self.textEdit.setVisible(True)
        self.closeBtn.setEnabled(True)
        print("ECode: " + str(error_code) + "\n")
        print("EDetail: " + error_details + "\n")

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
            #TODO to be tested
            self.trans2.set_debconf_frontend('kde')
            '''
            Can't exec "debconf-kde-helper": No existe el archivo o el directorio at /usr/share/perl5/Debconf/FrontEnd/Kde.pm line 43.
Unable to execute debconf-kde-helper - is debconf-kde-helper installed?Can't exec "debconf-kde-helper": No existe el archivo o el directorio at /usr/share/perl5/Debconf/FrontEnd/Kde.pm line 43.
Unable to execute debconf-kde-helper - is debconf-kde-helper installed?'''
            #self.trans2.set_debconf_frontend('gnome')
            '''
            debconf: no se pudo inicializar la interfaz: Gnome
debconf: (Can't locate Gtk3.pm in @INC (you may need to install the Gtk3 module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.28.1 /usr/local/share/perl/5.28.1 /usr/lib/x86_64-linux-gnu/perl5/5.28 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl/5.28 /usr/share/perl/5.28 /usr/local/lib/site_perl /usr/lib/x86_64-linux-gnu/perl-base) at /usr/share/perl5/Debconf/FrontEnd/Gnome.pm line 151.)
debconf: probando ahora la interfaz: Dialog
debconf: no se pudo inicializar la interfaz: Dialog
debconf: (La interfaz «dialog» no funcionará en un terminal tonto, un búfer de intérprete de órdenes de emacs, o sin una terminal controladora.)
debconf: probando ahora la interfaz: Readline
'''
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
