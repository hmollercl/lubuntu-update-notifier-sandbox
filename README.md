# lubuntu-update-notifier
Depend on:
update-notifier-common ( https://packages.ubuntu.com/disco/update-notifier-common )
aptdaemon

notifier.py chek on demand if upgrades exist or if restart is needed.
To check if upgrades exists calls update_worker.py which uses apt_check from update-notifier-common.
Cache update is run periodically by update-notifier-common.
If there are upgrades pressing "upgrade button" calls upgrader.py w/o options or modifiers. 
This is, no cache update is done and safe-upgrade or "apt upgrade" is done, NOT full upgrade or "dist-upgrade"

upgrader.py can be called directly to upgrade the system.
it has 2 options whcih can be readed with --help.
The options are:
  --cache-update  Update Cache Before Upgrade
  --full-upgrade  Full upgrade same as dist-upgrade
