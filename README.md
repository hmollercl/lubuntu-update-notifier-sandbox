# lubuntu-update-notifier
Installation Instruction:
Install packages (via apt or similar):
- update-notifier-common
- aptdaemon

This files are the ones that need to be downloaded and need to be copied in the same directory, the files are:
- notifier.py
- update_worker.py
- upgrader.py
- upNot.sh

run upNot.sh to check every hour if there are updates. It's recommended to add an entry in autostart. By going to:
Preferences -> LXQt configuration -> Sesion confuiguration
There you got to autosart, pres add, in Name put something like "Update Notifier" in Comand search for upNot.sh done.

---------------------------------------------------------------------------------------------------------------------

Depend on:
- update-notifier-common ( https://packages.ubuntu.com/disco/update-notifier-common )
- aptdaemon
- debconf-kde-helper

notifier.py chek on demand if upgrades exist or if restart is needed.
To check if upgrades exists it calls update_worker.py which uses apt_check from update-notifier-common.
Cache update is run periodically by update-notifier-common.
If there are upgrades pressing "upgrade button" calls defined upgrade software w/o options or modifiers.
This is, no cache update is done and safe-upgrade or "apt upgrade" is done, NOT full upgrade or "dist-upgrade"
upgrade software is defined with -u. Example:
$./notifier.py -u ./upgrader.py

upgrader.py can be called directly to upgrade the system.
it has 2 options whcih can be readed with --help.
The options are:
  --cache-update  Update Cache Before Upgrade
  --full-upgrade  Full upgrade same as dist-upgrade

to run it periodically the upNot.sh script can run in the back.
