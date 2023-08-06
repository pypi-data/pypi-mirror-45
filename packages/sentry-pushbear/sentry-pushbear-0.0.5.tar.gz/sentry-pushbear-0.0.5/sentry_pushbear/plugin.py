#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sentry-PushBear
"""
import logging

from django import forms
from sentry.http import safe_urlopen
from sentry.plugins.bases import notify

import sentry_pushbear


class PushBearSettingsForm(notify.NotificationConfigurationForm):
    SendKey = forms.CharField(
        label='PushBear SendKey',
        widget=forms.TextInput(attrs={'placeholder': '12000-00000000000000000000000000000000'}),
        help_text='Your SendKey. See http://pushbear.ftqq.com/'
    )


class PushBearNotifications(notify.NotificationPlugin):
    title = 'PushBear Notifications'
    slug = 'sentry_pushbear'
    author = 'Woko'
    author_url = 'https://github.com/WokoLiu/sentry-pushbear'

    conf_title = title
    conf_key = 'sentry_pushbear'

    resource_links = [
        ('Bug Tracker', 'https://github.com/WokoLiu/sentry-pushbear/issues'),
        ('Source', 'https://github.com/WokoLiu/sentry-pushbear'),
    ]

    version = sentry_pushbear.VERSION
    project_conf_form = PushBearSettingsForm

    logger = logging.getLogger('sentry.plugins.sentry_pushbear')

    def can_enable_for_projects(self):
        return True

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('SendKey', project))

    def get_config(self, project, **kwargs):
        return [
            {
                'name': 'SendKey',
                'label': 'PushBear SendKey',
                'type': 'text',
                'help': 'Your SendKe. See http://pushbear.ftqq.com/',
                'placeholder': '12000-00000000000000000000000000000000',
                'validators': [],
                'required': True,
            }
        ]

    def notify_users(self, group, event, fail_silently=False, **kwargs):
        self.logger.debug('Received notification for event: %s' % event)
        project = group.project

        title = '%s: %s' % (project.name, group.title)
        link = group.get_absolute_url()

        culprit = group.culprit
        message = event.message
        tags = event.get_tags()

        if tags:
            tags = '\n\n'.join('%s: %s' % (k, v) for k, v in tags)
        else:
            tags = ''

        # see http://pushbear.ftqq.com/admin/#/api
        data = {
            'sendkey': self.get_option('SendKey', project),
            'text': title,
            'desp': ('## Project\n'
                     '%s\n'
                     '## Culprit\n'
                     '%s\n'
                     '## Message\n'
                     '[%s](%s)\n'
                     '## Tags\n'
                     '%s'
                     % (project.name, culprit, message, link, tags)),
        }

        rv = safe_urlopen(method='POST',
                          url='https://pushbear.ftqq.com/sub',
                          data=data)
        if not rv.ok:
            raise RuntimeError('Failed to notify: %s' % rv)
