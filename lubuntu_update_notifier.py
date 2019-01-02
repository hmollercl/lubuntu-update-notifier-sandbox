#!/usr/bin/python3

import sys
import apt
#import apt_pkg
#import apt.progress
from PyQt5.QtWidgets import (QWidget, QApplication, QDialog)
from PyQt5 import uic
from PyQt5.QtCore import (QProcess)

'''
cand_ver = depcache.get_candidate_ver(pkg)
if isSecurityUpgrade(cand_ver):
                upgrades += 1
                security_updates += 1
                continue



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
'''

'''
for upg_pkg in cache.get_changes():
    pkg = cache[upg_pkg.name]
    print(pkg)
    #upgrade_short_name.append(pkg.name)

#cache.commit(apt.progress.TextFetchProgress(), apt.progress.InstallProgress())
#upgrade_short_name.append(cache.get_changes().name
print(upgrade_short_name)
#después con aptdaemon instalarlos que tiene connect
'''
class Dialog(QWidget):
    def __init__(self, cache):
        QWidget.__init__(self)
        uic.loadUi("designer/update_notifier.ui", self)
        #self.initUI()
        self.buttonBox.accepted.connect(self.call_update_software)
        self.buttonBox.rejected.connect(self.call_reject)
        #self.pkg_number=pkg_number
        pkgs=cache.get_changes()
        print(pkgs)
        print(len(pkgs))
        
    def call_update_software(self):
        program = "plasma-discover"
        arguments = {"--mode", "Update"}
        process = QProcess()
        process.setProgram(program)
        process.setArguments(arguments)
        process.startDetached()
        process.start()
        process.waitForStarted()
        app.quit()
        
    def call_reject(self):
        app.quit()

class App(QApplication):
    def __init__(self, cache, *args,):
        QApplication.__init__(self, *args)
        #self.pkg_number = pkg_number
        self.dialog = Dialog(cache)
        self.dialog.show()

def main(args, cache):
    global app
    app = App(cache, args)
    #print(pkg_number)
    app.exec_()

if __name__ == "__main__":
    cache = apt.Cache()
    cache.update()
    cache.open(None)
    cache.upgrade(dist_upgrade = True)

    pkgs=cache.get_changes()
    pkg_number = len(pkgs)
    
    if pkg_number > 0:
        main(sys.argv, cache)

