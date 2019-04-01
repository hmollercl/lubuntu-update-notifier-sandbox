# lubuntu-update-notifier
Installation Instruction:
Install packages (via apt or similar):
- update-notifier-common
- aptdaemon
- debconf-kde-helper

This files are the ones that need to be downloaded and need to be copied in the same directory, the files are:
- notifier.py
- upgrader.py
- upNot.sh
- update_worker.py

run upNot.sh to check every hour if there are updates. It's recommended to add an entry in autostart. By going to:
Preferences -> LXQt configuration -> Sesion confuiguration
There you got to autosart, pres add, in Name put something like "Update Notifier" in Comand search for upNot.sh

---------------------------------------------------------------------------------------------------------------------

Depend on:
- update-notifier-common ( https://packages.ubuntu.com/disco/update-notifier-common )
- aptdaemon
- debconf-kde-helper

- upNot.sh
Chek every hour if upgrades exist or if restart is needed.
To check if upgrades exists it uses apt_check from update-notifier-common.
Cache update is run periodically by update-notifier-common.
If there are upgrades it calls notifier_gui.py using this command:
./notifier.py -p ./upgrader.py


- notifier.py
this script has 1 options that can be readed with --help:
	-p for the upgrade programm to use.
Pressing "upgrade button" calls the upgrade software defined with -p.
No cache update is done and safe-upgrade or "apt upgrade" is done, NOT full upgrade or "dist-upgrade"

- upgrader.py
This can be called directly to upgrade the system.
it has 2 options which can be readed with --help.
The options are:
  --cache-update  Update Cache Before Upgrade
  --full-upgrade  Full upgrade same as dist-upgrade
