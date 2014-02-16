#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
import urllib
from kitnirc.modular import Module
from botparse import BotParse
import yaml
import datetime
import urllib
from itertools import takewhile
 
_log = logging.getLogger(__name__)

parser = BotParse()
command_events = parser.add_command('!events')
command_events.add_argument('--limit', type=int)
command_today = parser.add_command('!today')
command_today.add_argument('--limit', type=int)
command_tomorrow = parser.add_command('!tomorrow')
command_tomorrow.add_argument('--limit', type=int)
command_next = parser.add_command('!next')

class AcmBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def messages(self, client, actor, recipient, message):
    
        self.client = client
        self.actor = actor
        self.recipient = recipient
        self.message = message

        config = self.controller.config

        # Only pay attention if addressed directly in channels
        try:
            self.args = parser.parse_args(self.message.split())
        except (NameError, TypeError):
            _log.debug("message not reconized %r", self.message)
            return

        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", self.actor, self.recipient)
        
        if self.args.command == "!events":
            if self.args.help:
                messages = command_events.format_help().split('\n')
            else:
                def sort(events):
                    events = sorted(events, key=lambda x: x['date'], reverse=True)
                    events = list(enumerate(takewhile(
                        lambda x: x['date'] >= datetime.date.today(),
                        events,
                    )))
                    return events
                messages = self.get_event_messages(sort)
        
        elif self.args.command == '!today':
            if self.args.help:
                messages = command_events.format_help().split('\n')
            else:
                def today_sort(events):
                    events = sorted(events, key=lambda x: x['date'], reverse=True)
                    events = list(enumerate(takewhile(
                        lambda x: x['date'] >= datetime.date.today(),
                        events,
                    )))
                    events = filter(
                        lambda (i, event): event['date'] == datetime.date.today(),
                        events
                    )
                    return events
                messages = self.get_event_messages(today_sort)

        elif self.args.command == '!tomorrow':
            if self.args.help:
                messages = command_events.format_help().split('\n')
            else:
                def tomorrow_sort(events):
                    events = sorted(events, key=lambda x: x['date'], reverse=True)
                    events = list(enumerate(takewhile(
                        lambda x: x['date'] >= datetime.date.today() + datetime.timedelta(days=1),
                        events,
                    )))
                    events = filter(
                        lambda (i, event): event['date'] == datetime.date.today() + datetime.timedelta(days=1),
                        events
                    )
                    return events
                messages = self.get_event_messages(tomorrow_sort)

        elif self.args.command == '!next':
            if self.args.help:
                messages = command_events.format_help().split('\n')
            else:
                def tomorrow_sort(events):
                    events = sorted(events, key=lambda x: x['date'], reverse=True)
                    events = list(enumerate(takewhile(
                        lambda x: x['date'] >= datetime.date.today(),
                        events,
                    )))
                    return [ events[-1] ]
                messages = self.get_event_messages(tomorrow_sort)

        elif self.args.command == "!help":
            messages = parser.format_help().split('\n')
        
        # send messages
        for message in messages:
            self.client.reply(self.recipient, self.actor, message)

        # Stop any other modules from handling this message.
        return True

    def get_event_messages(self, func=None):
        config = self.controller.config
        
        if not config.has_section("acmbot"):
            _log.info("No config section for acmbot")
            return

        if config.has_option("acmbot", "base_url"):
            base_url = config.get("acmbot", "base_url")
        else:
            return

        if getattr(self.args, 'limit', None):
            events_limit = self.args.limit
        elif config.has_option("acmbot", "events_limit"):
            try:
                events_limit = int(config.get("acmbot", "events_limit"))
            except TypeError:
                events_limit = None
        else:
            events_limit = None

        events_html = urllib.urlopen(
            '{}/files/events.yaml'.format(base_url)
        ).read()

        events = yaml.load(events_html)
        length_events = len(events)

        if func:
            events = func(events)
        
        if events_limit and events_limit >= 0:
            events = events[len(events)-events_limit:]
        
        messages = []
        for i, event in reversed(events):
            
            if 'time' in event:
                time = get_time(event['time'])
            elif config.has_option("acmbot", "default_time"):
                time = get_time(config.get("acmbot", "default_time"))
            else:
                time = None

            message = '{} - {:%a, %b %d}'.format(
                event['title'], event['date'],
            )

            if time:
                message += ' @ {:%I:%M%p}'.format(time)

            message += ' - {}/event.php?event={}'.format(
                base_url, str(length_events - i - 1),
            )

            messages.append(message)
        return messages

def get_time(time_str):
    return datetime.datetime.strptime(time_str, '%H:%M').time()
    
module = AcmBotModule
