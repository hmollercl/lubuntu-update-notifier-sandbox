#!/usr/bin/env python3

from setuptools import setup

setup(
    name="lubuntu-update-notifier",
    version="0.1",
    packages=['lubuntu-update-notifier'],
    #scripts=['notifier.py','upgrader.py'],
    scripts=['upg-notifier.sh'],
#    data_files=[
#                  ('/etc/xdg/autostart',
#                   ['upgNotifier.sh', ]
#                  ),
#                  ],
)
