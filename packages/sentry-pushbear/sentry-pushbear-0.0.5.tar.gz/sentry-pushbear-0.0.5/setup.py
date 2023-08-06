#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sentry_pushbear

setup(
    name='sentry-pushbear',
    version=sentry_pushbear.VERSION,
    author='Woko',
    author_email='banbooliu@gmail.com',
    url='https://github.com/WokoLiu/sentry-pushbear',
    description='A Sentry plugin that integrates with pushbear to send to wecaht',
    long_description=__doc__,
    license='GPL-3.0',
    packages=find_packages(),
    entry_points={
        'sentry.plugins': [
            'sentry_pushbear = sentry_pushbear.plugin:PushBearNotifications'
        ]
    },
    include_package_data=True,
)