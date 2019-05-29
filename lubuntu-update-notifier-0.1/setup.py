#!/usr/bin/env python3

#from setuptools import setup
from distutils.core import setup
#import setuptools
#setuptools  # pyflakes
#from DistUtilsExtra.auto import setup
from DistUtilsExtra.command import *

setup(
    name="lubuntu-update-notifier",
    version="0.1",
    packages=['lubuntu-update-notifier'],
    scripts=['upg-notifier.sh'],
    cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" :  build_help.build_help,
                   "build_icons" :  build_icons.build_icons }
)
