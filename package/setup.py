#!/usr/bin/env python3

from setuptools import setup

setup(
    name="lubuntu-update-notifier",
    version="0.1",
    #packages=find_packages(),
    packages=['lubuntu-update-notifier'],
    scripts=['notifier.py','upgrader.py'],
    #data_files=['lib/lubuntu-update-notifier/'],

)
