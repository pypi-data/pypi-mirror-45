# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Description :
   Author :       CoolCat
   date：          2019/4/29
-------------------------------------------------
   Change Activity:
                   2019/4/29:
-------------------------------------------------
"""
__author__ = 'CoolCat'

from distutils.core import setup

setup(
    name='filemon',
    version='0.0.4',
    author='CoolCat',
    author_email='27958875@qq.com',
    packages=['filemon'],
    scripts=['filemon/filemon.py'],
    url='https://github.com/TheKingOfDuck/FileMonitor',
    description='A file monitor tool compatible with Windows, Linux,  And MacOS.',
    install_requires=[
        "watchdog",
        "filemon",
    ],
)