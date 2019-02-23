#!/usr/bin/python3
# based on apt_check.py
# or
# we could use update-notifier-common https://packages.ubuntu.com/disco/update-notifier-common
#
import sys
import apt
import apt_pkg
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton,
							QHBoxLayout, QVBoxLayout, QProgressBar, QTreeView,
							 QTextEdit, QMessageBox)
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
    def __init__(self, depcache, cache, upgrades, security_updates):
        QWidget.__init__(self)
        #uic.loadUi("designer/update_notifier.ui", self)
        self.upgrades = upgrades

        self.initUI()
        self.closeBtn.clicked.connect(self.call_reject)
        self.apt_client = client.AptClient()
        self.downloadText = ""
        self.detailText = ""

        #self.upgrade_swBtn.clicked.connect(self.call_update_software)
        self.upgradeBtn.clicked.connect(self.upgrade)

        '''
        if options.fullUpgrade:
            self.trans2 = self.apt_client.upgrade_system(safe_mode=False)
        else:
            self.trans2 = self.apt_client.upgrade_system(safe_mode=True)

        if options.cacheUpdate:
            self.trans1 = self.apt_client.update_cache()
            self.update_cache()
        else:
            self.upgrade()
        '''
    def initUI(self):

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        self.upgradeBtn = QPushButton("Upgrade")
        self.closeBtn = QPushButton("Close")
        self.progressBar = QProgressBar()
        self.textEdit = QTextEdit()
        self.treeView = QTreeView()

        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.closeBtn)
        hbox.addWidget(self.upgradeBtn)
        hbox.addStretch(1)

        vbox=QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.treeView)
        vbox.addWidget(self.progressBar)
        vbox.addWidget(self.textEdit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 500, 150)
        self.setWindowTitle('Upgrade')#TODO
        self.progressBar.setVisible(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setVisible(False)

        if self.upgrades > 0:
            self.label.setText("There are %s upgrades available and %s security updates available, do you want to Upgrade? \n The following are the affected packages:" % (upgrades, security_updates))
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

    def upgrade_progress(self, transaction, progress):
        self.upgradeBtn.setVisible(False)
        #self.upgrade_swBtn.setVisible(False)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        #self.label.setText("Applying changes...")


    def upgrade_progress_download(self, transaction, uri, status, short_desc,
                                  total_size, current_size, msg):
        self.textEdit.setVisible(True)
        #self.downloadText = "Downloading " + short_desc
        #self.label.setText(self.detailText + "\n" + self.downloadText)
        self.textEdit.append(status + " " + short_desc + " " + str(current_size) + "/" + str(total_size) + " " + msg)
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
            self.textEdit.setVisible(True)
            if self.detailText != "Downloaded " + str(current_items) + " of " + str(total_items):
                self.detailText = "Downloaded " + str(current_items) + " of " + str(total_items)
                self.label.setText(self.detailText + "\n" + self.downloadText)
                self.textEdit.append(self.detailText + "\n" + self.downloadText)

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

        if(len(self.errors)>0):
            text = text + " with some errors:"

        self.label.setText(text)
        self.closeBtn.setVisible(True)
        self.upgradeBtn.setVisible(False)
        #self.upgrade_swBtn.setVisible(False)
        self.closeBtn.setEnabled(True)

    def upgrade_error(self, transaction, error_code, error_details):
        self.upgradeBtn.setVisible(False)
        self.upgrade_swBtn.setVisible(False)
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

    def createViewModel(self,parent):
        model = QStandardItemModel(0 , 2, parent)
        model.setHeaderData(0, Qt.Horizontal, "Action")
        model.setHeaderData(1, Qt.Horizontal, "Package")
        return model

    '''def call_update_software(self):
        program = "plasma-discover"
        arguments = {"--mode", "Update"}
        process = QProcess()
        process.setProgram(program)
        process.setArguments(arguments)
        process.startDetached()
        process.start()
        process.waitForStarted()
        #app.quit()
        '''
        '''
        fprogress = apt.progress.base.FetchProgress()
        iprogress = apt.progress.base.InstallProgress()
        depcache.commit(fprogress, iprogress)
        '''
    def upgrade(self):
        self.progressBar.setVisible(False)
        #TODO ¿Hacerlo paquete a paquete pare que hay más/mejor info?
        self.treeView.setVisible(False)
        self.errors = []
        self.label.setText("Applying changes...")

        self.apt_client = client.AptClient()
        try:
            self.trans2 = self.apt_client.commit_packages(install=self.install_pkgs, remove=self.remove_pkgs, reinstall=[], purge=[], upgrade=self.upgrade_pkgs, downgrade=[])
            #self.trans2 = self.apt_client.upgrade_system(safe_mode=False)
            self.trans2.connect('progress-changed', self.upgrade_progress)
            self.trans2.connect('cancellable-changed',
                                     self.upgrade_cancellable_changed)
            self.trans2.connect('progress-details-changed',
                                     self.upgrade_progress_detail)
            self.trans2.connect('progress-download-changed',
                                     self.upgrade_progress_download)
            self.trans2.connect('finished', self.upgrade_finish)
            self.trans2.connect('error', self.upgrade_error)
            self.trans2.set_debconf_frontend('kde')
            self.trans2.run()

        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully:" +
                  "{}".format(e))

    def call_reject(self):
        app.quit()

class App(QApplication):
    def __init__(self, depcache, cache, upgrades, security_updates, *args):
        QApplication.__init__(self, *args)
        self.dialog = Dialog(depcache, cache, upgrades, security_updates)
        self.dialog.show()


def main(args, depcache, cache, upgrades, security_updates):
    global app
    app = App(depcache, cache, upgrades, security_updates, args)
    app.setWindowIcon(QIcon.fromTheme("system-software-update"))
    app.exec_()

############################ END QT############################################
SYNAPTIC_PINFILE = "/var/lib/synaptic/preferences"
DISTRO = subprocess.check_output(
    ["lsb_release", "-c", "-s"],
    universal_newlines=True).strip()

def _(msg):
    return gettext.dgettext("update-notifier", msg)


def _handleException(type, value, tb):
    sys.stderr.write("E: " + _("Unknown Error: '%s' (%s)") % (type, value))
    sys.exit(-1)


def clean(cache, depcache):
    " unmark (clean) all changes from the given depcache "
    # mvo: looping is too inefficient with the new auto-mark code
    # for pkg in cache.Packages:
    #     depcache.MarkKeep(pkg)
    depcache.init()

def saveDistUpgrade(cache, depcache):
	#TODO depending on modifier do both.
    """ this function mimics a upgrade but will never remove anything, unless clean is commented"""
    depcache.upgrade(True)
    '''if depcache.del_count > 0:
        clean(cache, depcache)
    depcache.upgrade()'''

def isSecurityUpgrade(ver):
    " check if the given version is a security update (or masks one) "
    security_pockets = [("Ubuntu", "%s-security" % DISTRO),
                        ("gNewSense", "%s-security" % DISTRO),
                        ("Debian", "%s-updates" % DISTRO)]
    for (file, index) in ver.file_list:
        for origin, archive in security_pockets:
            if (file.archive == archive and file.origin == origin):
                return True
    return False

def init():
    " init the system, be nice "
    # FIXME: do a ionice here too?
    os.nice(19)
    apt_pkg.init()


def run():

    # we are run in "are security updates installed automatically?"
    # question mode
    '''
    if options.security_updates_unattended:
        res = apt_pkg.config.find_i("APT::Periodic::Unattended-Upgrade", 0)
        # print(res)
        sys.exit(res)
    '''
    '''
     if options.update_cache
        apt_client = client.AptClient()
        trans = apt_client.update_cache(wait=True)
    '''
    # get caches
    try:
        cache = apt_pkg.Cache(apt.progress.base.OpProgress())
    except SystemError as e:
        sys.stderr.write("E: " + _("Error: Opening the cache (%s)") % e)
        sys.exit(-1)
    depcache = apt_pkg.DepCache(cache)

    # read the synaptic pins too
    if os.path.exists(SYNAPTIC_PINFILE):
        depcache.read_pinfile(SYNAPTIC_PINFILE)
        depcache.init()

    if depcache.broken_count > 0:
        sys.stderr.write("E: " + _("Error: BrokenCount > 0"))
        sys.exit(-1)

    # do the upgrade (not dist-upgrade!)
    try:
        saveDistUpgrade(cache, depcache)
    except SystemError as e:
        sys.stderr.write("E: " + _("Error: Marking the upgrade (%s)") % e)
        sys.exit(-1)

    # analyze the ugprade
    upgrades = 0
    security_updates = 0

    # we need another cache that has more pkg details
    with apt.Cache() as aptcache:
        for pkg in cache.packages:
            # skip packages that are not marked upgraded/installed
            if not (depcache.marked_install(pkg)
                    or depcache.marked_upgrade(pkg)):
                continue
            # check if this is really a upgrade or a false positive
            # (workaround for ubuntu #7907)
            inst_ver = pkg.current_ver
            cand_ver = depcache.get_candidate_ver(pkg)
            if cand_ver == inst_ver:
                continue
            # check for security upgrades
            if isSecurityUpgrade(cand_ver):
                upgrades += 1
                security_updates += 1
                continue

            # check to see if the update is a phased one
            try:
                from UpdateManager.Core.UpdateList import UpdateList
                ul = UpdateList(None)
                ignored = ul._is_ignored_phased_update(
                    aptcache[pkg.get_fullname()])
                if ignored:
                    depcache.mark_keep(pkg)
                    continue
            except ImportError:
                pass

            upgrades = upgrades + 1

            # now check for security updates that are masked by a
            # candidate version from another repo (-proposed or -updates)
            for ver in pkg.version_list:
                if (inst_ver
                        and apt_pkg.version_compare(ver.ver_str,
                                                    inst_ver.ver_str) <= 0):
                    continue
                if isSecurityUpgrade(ver):
                    security_updates += 1
                    break

        # print the number of regular upgrades and the number of
        # security upgrades
        #sys.stderr.write("%s;%s" % (upgrades, security_updates))
        print("%s;%s" % (upgrades, security_updates))

    # return the number of upgrades (if its used as a module)
    return(depcache, cache, upgrades, security_updates)



if __name__ == "__main__":
    #sys.excepthook = _handleException

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

    # gettext
    APP = "update-notifier"
    DIR = "/usr/share/locale"
    gettext.bindtextdomain(APP, DIR)
    gettext.textdomain(APP)

    global reboot_required_path
    reboot_required_path = Path("/var/run/reboot-required")

    init()
    (depcache, cache, upgrades, security_updates) = run()

    if upgrades > 0:
        main(sys.argv, depcache, cache, upgrades, security_updates)

    # check "/var/run/reboot-required" (.pkgs) if exists reboot is needed.
    if reboot_required_path.exists():
        main(sys.argv, depcache, cache, 0, 0)

