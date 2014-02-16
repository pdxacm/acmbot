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
command_day = parser.add_command('!day')
command_day.add_argument('--limit', type=int)
command_day.add_argument(
    'day',
    nargs=1,
    choices=[
        'monday', 'tuesday', 'wednesday', 'thursday', 
        'friday', 'saturday', 'sunday',
        ],
    default=None,
)

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
        
        messages = []

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

        elif self.args.command == '!day':
            if self.args.help:
                messages = command_events.format_help().split('\n')
            elif self.args.day:
                # The date to filter by will be constructed.

                today = datetime.date.today()
                
                # Get the int encoding of the day of the week.
                # Monday = 0 ... Sunday = 6
                today_weekday = today.weekday()


                wanted_weekday = [
                    'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday', 'sunday',
                ].index(self.args.day[0].lower())

                if wanted_weekday >= today_weekday:
                    # If today is Wednesday and Wednesday is wanted then
                    # the day should not be changed.
                    #     Wednesday - Wednesday = 2 - 2 = 0
                    # If today is Tuesday and Friday is wanted then
                    # the day should be increased by 3
                    #     Friday - Tuesday = 4 - 1 = 3
                    days = wanted_weekday - today_weekday
                else:
                    # If today is Friday and Monday is wanted then the
                    # day should be increased by 3.
                    #    7 - Friday + Monday = 7 - 4 + 0 = 3 
                    # If today is Thursday and Tuesday is wanted then the
                    # day should be increased by 5.
                    #    7 - Thursday + Tuesday = 7 - 3 + 1 = 5
                    days = 7 - today_weekday + wanted_weekday
            
                # Construct the date by adding the calculated number of
                # days.
                date = today + datetime.timedelta(days=days)

                def day_sort(events):
                    events = sorted(events, key=lambda x: x['date'], reverse=True)
                    events = list(enumerate(takewhile(
                        lambda x: x['date'] >= date,
                        events,
                    )))
                    events = filter(
                        lambda (i, event): event['date'] == date,
                        events
                    )
                    return events
                messages = self.get_event_messages(day_sort)

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
        
        if events_limit and events_limit >= 0 and len(events) >= events_limit:
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
