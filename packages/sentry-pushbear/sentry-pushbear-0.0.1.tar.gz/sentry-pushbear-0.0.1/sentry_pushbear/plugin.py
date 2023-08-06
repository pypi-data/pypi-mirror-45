#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sentry-PushBear
"""

from django import forms
from sentry.http import safe_urlopen
from sentry.plugins.bases.notify import NotifyPlugin

import sentry_pushbear


class PushBearSettingsForm(forms.Form):
    SendKey = forms.CharField(
        help_text='Your SendKey. See http://pushbear.ftqq.com/')


class PushBearNotifications(NotifyPlugin):
    author = 'Woko'
    author_url = 'https://github.com/WokoLiu'

    title = 'PushBear'

    conf_title = 'PushBear'
    conf_key = 'pushbear'
    slug = 'pushbear'

    resource_links = [
        ('Bug Tracker', 'https://github.com/WokoLiu/sentry-pushbear/issues'),
        ('Source', 'https://github.com/WokoLiu/sentry-pushbear'),
    ]

    version = sentry_pushbear.VERSION
    project_conf_form = PushBearSettingsForm

    def can_enable_for_projects(self):
        return True

    def is_configured(self, project):
        return bool(self.get_option('SendKey', project))

    def notify(self, notification):
        event = notification.event
        group = event.group
        project = group.project

        title = '%s: %s' % (project.name, group.title)
        link = group.get_absolute_url()

        culprit = group.culprit

        tags = event.get_tags()

        message = event.message + '\n'
        if tags:
            message = 'Tags: %s\n' % (', '.join(
                '%s=%s' % (k, v) for (k, v) in tags))

        # see http://pushbear.ftqq.com/admin/#/api
        data = {
            'sendkey': self.get_option('SendKey', project),
            'text': title,
            'desp': ('### culprit\n'
                     '%s\n'
                     '### message\n'
                     '[%s](%s)'
                     % (culprit, message, link)),
        }

        rv = safe_urlopen('https://pushbear.ftqq.com/sub',
                          data=data)
        if not rv.ok:
            raise RuntimeError('Failed to notify: %s' % rv)

            # try:
            #     res = rv.json()
            #     if res['code'] != 0:
            #         raise RuntimeError('Failed to notify: %s' % res['message'])
            # except (AttributeError, KeyError) as e:
            #     raise RuntimeError('Failed to notify: %s' % e)
