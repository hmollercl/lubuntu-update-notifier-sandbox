#!/usr/bin/python3
#based on apt_check.py

import sys
import apt
import apt_pkg
#import apt.progress.base
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog)
from PyQt5 import uic
from PyQt5.QtCore import (Qt, QProcess)
from PyQt5.QtGui import (QStandardItemModel, QIcon)
import os
from optparse import OptionParser
import gettext
import subprocess

from aptdaemon import client
from aptdaemon.errors import NotAuthorizedError, TransactionFailed

'''
class UpdateDialog(QDialog): #último popUp
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designer/update_dialog.ui", self)
        self.buttonBox.accepted.connect(self.aceptar)
        
    def aceptar(self):
        app.quit()
        
        
    def on_driver_changes_progress(self, transaction, progress):
        #self.button_driver_revert.setVisible(False)
        #self.button_driver_apply.setVisible(False)
        #self.button_driver_restart.setVisible(False)
        #self.buttonBox.rejected.setVisible(True)
        #self.progressBar.setVisible(True)

        #self.label.setText("Applying changes...")
        self.progressBar.setValue(progress)

    def on_driver_changes_finish(self, transaction, exit_state):
        Dialog.label.setText("Installation Complete")
        #self.progress_bar.setVisible(False)
        #self.clear_changes()
        #self.apt_cache = apt.Cache()
        #self.set_driver_action_status()
        #self.update_label_and_icons_from_status()
        #self.button_driver_revert.setVisible(True)
        #self.button_driver_apply.setVisible(True)
        #self.button_driver_cancel.setVisible(False)
        self.buttonBox.rejected.setVisible(False)
        #self.scrolled_window_drivers.set_sensitive(True)

    def on_driver_changes_error(self, transaction, error_code, error_details):
        #self.on_driver_changes_revert()
        #self.set_driver_action_status()
        #self.update_label_and_icons_from_status()
        #self.button_driver_revert.setVisible(True)
        #self.button_driver_apply.setVisible(True)
        self.button_driver_cancel.setVisible(False)
        #self.scrolled_window_drivers.set_sensitive(True)

  def on_driver_changes_cancellable_changed(self, transaction, cancellable):
    self.button_driver_cancel.setEnabled(cancellable)

        self.apt_client = client.AptClient()
        try:
            self.transaction = self.apt_client.commit_packages(install=install_pkgs, remove=remove_pkgs, reinstall=[], purge=[], upgrade=upgrade_pkgs, downgrade=[])
            self.transaction.connect('progress-changed', self.progress)
            self.transaction.connect('cancellable-changed', self.cancellable_changed)
            progress-download-changed → uri, short_desc, total_size, current_size, msg
            self.transaction.connect('finished', self.finish)
            self.transaction.connect('error', self.error)
            self.transaction.run()
        
        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully: {}".format(e))
'''
class Dialog(QWidget):
    def __init__(self, depcache, cache, upgrades, security_updates):
        QWidget.__init__(self)
        uic.loadUi("designer/update_notifier.ui", self)
        self.initUI()
        self.buttonBox.accepted.connect(self.call_update_software)
        #self.buttonBox.Open.connect(self.call_update_software)
        self.buttonBox.rejected.connect(self.call_reject)
        
    def initUI(self):
        self.label.setText("There are %s upgrades available and %s security updates available, do you want to open the Update Software? \n The following are the affected packages" % (upgrades, security_updates))
        #self.label.setText("There are %s upgrades available and %s security updates available, do you want to Update? \n The following are the affected packages:" % (upgrades, security_updates))
        self.model = self.createViewModel(self)
        self.treeView.setModel(self.model)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        self.progressBar.setVisible(False)
        
        self.install_pkgs = []
        self.remove_pkgs = []
        self.upgrade_pkgs = []
        
        for pkg in cache.packages:
            if depcache.marked_install(pkg):
                self.model.insertRow(0)
                self.model.setData(self.model.index(0, 0), "Install")
                self.model.setData(self.model.index(0, 1), pkg.name)
                install_pkgs.append(pkg.name)
            elif depcache.marked_upgrade(pkg):
                self.model.insertRow(0)
                self.model.setData(self.model.index(0, 0), "Upgrade")
                self.model.setData(self.model.index(0, 1), pkg.name)
                upgrade_pkgs.append(pkg.name)
            elif depcache.marked_delete(pkg):
                self.model.insertRow(0)
                self.model.setData(self.model.index(0, 0), "Delete")
                self.model.setData(self.model.index(0, 1), pkg.name)
                remove_pkgs.append(pkg.name)
        
        self.treeView.setSortingEnabled(True)
        self.treeView.sortByColumn(0,Qt.SortOrder())
        self.treeView.setSortingEnabled(False)
                #self.button_driver_revert.setVisible(False)
        #self.button_driver_apply.setVisible(False)
        #self.button_driver_restart.setVisible(False)
        #self.buttonBox.rejected.setVisible(True)
        #self.progressBar.setVisible(True)

        #self.label.setText("Applying changes...")
        self.progressBar.setValue(progress)

    def on_driver_changes_finish(self, transaction, exit_state):
        Dialog.label.setText("Installation Complete")
        #self.progress_bar.setVisible(False)
        #self.clear_changes()
        #self.apt_cache = apt.Cache()
        #self.set_driver_action_status()
        #self.update_label_and_icons_from_status()
        #self.button_driver_revert.setVisible(True)
        #self.button_driver_apply.setVisible(True)
        #self.button_driver_cancel.setVisible(False)
        self.buttonBox.rejected.setVisible(False)
        #self.scrolled_window_drivers.set_sensitive(True)

    def on_driver_changes_error(self, transaction, error_code, error_details):
        #self.on_driver_changes_revert()
        #self.set_driver_action_status()
        #self.update_label_and_icons_from_status()
        #self.button_driver_revert.setVisible(True)
        #self.button_driver_apply.setVisible(True)
        self.button_driver_cancel.setVisible(False)
        #self.scrolled_window_drivers.set_sensitive(True)

    def on_driver_changes_cancellable_changed(self, transaction, cancellable):
        self.button_driver_cancel.setEnabled(cancellable)

    def createViewModel(self,parent):
        model = QStandardItemModel(0 , 2, parent)
        model.setHeaderData(0, Qt.Horizontal, "Action")
        model.setHeaderData(1, Qt.Horizontal, "Package")
        return model
    
    def call_update_software(self):
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
        fprogress = apt.progress.base.FetchProgress()
        iprogress = apt.progress.base.InstallProgress()
        depcache.commit(fprogress, iprogress)
        '''
    def update(self)
        self.progressBar.setVisible(False)
        self.treeView.setVisible(False)
        
        self.apt_client = client.AptClient()
        try:
            self.transaction = self.apt_client.commit_packages(install=self.install_pkgs, remove=self.remove_pkgs, reinstall=[], purge=[], upgrade=self.upgrade_pkgs, downgrade=[])
            self.transaction.connect('progress-changed', self.progress)
            self.transaction.connect('cancellable-changed', self.cancellable_changed)
            #progress-download-changed → uri, short_desc, total_size, current_size, msg
            #progress-details-changed → current_items, total_items, currenty_bytes, total_bytes, current_cps, eta
            self.transaction.connect('finished', self.finish)
            self.transaction.connect('error', self.error)
            self.transaction.run()
        
        except (NotAuthorizedError, TransactionFailed) as e:
            print("Warning: install transaction not completed successfully: {}".format(e))
        
    def call_reject(self):
        app.quit()

class App(QApplication):
    def __init__(self, depcache, cache, upgrades, security_updates, *args):
        QApplication.__init__(self, *args)
        #self.pkg_number = pkg_number
        self.dialog = Dialog(depcache, cache, upgrades, security_updates)
        self.dialog.show()


def main(args, depcache, cache, upgrades, security_updates):
    global app
    app = App(depcache, cache, upgrades, security_updates, args)
    app.setWindowIcon(QIcon.fromTheme("system-software-update"))
    app.exec_()

############################ END QT#######################
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
    """ this function mimics a upgrade but will never remove anything unless clean is commented"""
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

    # gettext
    APP = "update-notifier"
    DIR = "/usr/share/locale"
    gettext.bindtextdomain(APP, DIR)
    gettext.textdomain(APP)
    
    init()
    (depcache, cache, upgrades, security_updates) = run()
        
    if upgrades > 0:
        main(sys.argv, depcache, cache, upgrades, security_updates)
