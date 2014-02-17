#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2014, Cameron White

import logging
import argparse
import urllib
from kitnirc.modular import Module
from botparse import BotParse
import yaml
import datetime
import urllib
from contextlib import closing
from itertools import takewhile, dropwhile
 
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

        self.read_config()

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
                messages = self.do_command(command_events)
        
        elif self.args.command == '!today':
            if self.args.help:
                messages = command_today.format_help().split('\n')
            else:
                messages = self.do_command(command_today)

        elif self.args.command == '!tomorrow':
            if self.args.help:
                messages = command_tomorrow.format_help().split('\n')
            else:
                messages = self.do_command(command_tomorrow)

        elif self.args.command == '!next':
            if self.args.help:
                messages = command_next.format_help().split('\n')
            else:
                messages = self.do_command(command_next)

        elif self.args.command == '!day':
            if self.args.help:
                messages = command_day.format_help().split('\n')
            elif self.args.day:
                messages = self.do_command(
                    lambda events: command_day(events, self.args.day),
                )

        elif self.args.command == "!help":
            messages = parser.format_help().split('\n')
        
        # send messages
        for message in messages:
            self.client.reply(self.recipient, self.actor, message)

        # Stop any other modules from handling this message.
        return True
        
    def do_command(self, command):

        events = self.get_events()
        
        events = command(events)

        config = self.controller.config

        if hasattr(self.args, 'limit'):
            events_limit = self.args.limit
        elif config.has_option("acmbot", "events_limit"):
            try:
                events_limit = int(config.get("acmbot", "events_limit"))
            except TypeError:
                events_limit = None
        else:
            events_limit = None

        if events_limit and events_limit >= 0 and len(events) >= events_limit:
            events = events[len(events)-events_limit:]

        for i, event in reversed(events):
            yield self.construct_message(i, event)
    
    def construct_message(self, event_id, event):

        if 'time' in event:
            time = get_time(event['time'])
        else:
            time = None

        message = '{} - {:%a, %b %d}'.format(
            event['title'], event['date'],
        )

        if time:
            message += ' @ {:%I:%M%p}'.format(time)

        message += ' - {}/event.php?event={}'.format(
            self.base_url, str(self.number_of_events - event_id - 1),
        )

        return message


    def get_events(self):
        events = load_yaml(
            '{}/{}'.format(self.base_url, self.events_yaml_url)
        )
        self.number_of_events = len(events)
        return events

    def read_config(self):
        config = self.controller.config

        if not config.has_section("acmbot"):
            _log.error("config has no `acmbot` section")
            return

        if config.has_option("acmbot", "base_url"):
            self.base_url = config.get("acmbot", "base_url")
        else:
            _log.error("config `acmbot` section has no `base_url` option")
            return

        if config.has_option("acmbot", "events_yaml_url"):
            self.events_yaml_url = config.get("acmbot", "events_yaml_url")
        else:
            _log.error("config `acmbot` section has no `events_yaml_url")
            return


def load_yaml(url):
    with closing(urllib.urlopen(url)) as yaml_raw:
        return yaml.load(yaml_raw.read())

def select_events(events, filter_function):
    # Sort events from newest to oldest.
    # Attach an id to each event [(id, event)].
    events = enumerate(sort_events(events))
    # Apply filtering function
    events = filter_function(events)
    return list(events)

def sort_events(events):
    """ Sort events from newest to oldest """
    return sorted(events, key=lambda x: x['date'], reverse=True)

def filter_take_date_range(events, start_date, end_date):
    """ Events filter which takes events which dates in the range
    from start_date to end_date inclusively. start_date >= end_date.
    events must be a list of the form [(id, event)]. """
   
    if start_date:
        events = dropwhile(
            lambda x: x[1]['date'] > start_date,
            events
        )

    if end_date:
        events = takewhile(
            lambda x: x[1]['date'] >= end_date,
            events
        )

    return events

def filter_take_date(events, date):
    return filter_take_date_range(events, date, date)

def command_date(events, date):
    return select_events(
            events, 
            lambda x: filter_take_date(x, date)
    )

def command_today(events):
    date = datetime.date.today()
    return command_date(events, date)

def command_tomorrow(events):
    date = datetime.date.today() + datetime.timedelta(days=1)
    return command_date(events, date)

def command_day(events, weekday):
    # The date to filter by will be constructed.

    today = datetime.date.today()
    
    # Get the int encoding of the day of the week.
    # Monday = 0 ... Sunday = 6
    today_weekday = today.weekday()
    
    days = weekday_difference(today_weekday, weekday[0])

    # Construct the date by adding the calculated number of
    # days.
    date = today + datetime.timedelta(days=days)
    return command_date(events, date)

def command_events(events):
    date = datetime.date.today()
    return select_events(
            events, 
            lambda events: filter_take_date_range(events, None, date)
    )

def command_next(events):
    return command_events(events)[-1:]

def weekday_difference(from_weekday, to_weekday):

    def get_weekday_index(weekday):
        if weekday not in range(7):
            weekday = [
                'monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday',
            ].index(weekday.lower())
        return weekday
    
    from_weekday = get_weekday_index(from_weekday)
    to_weekday = get_weekday_index(to_weekday)

    if to_weekday >= from_weekday:
        # If from is Wednesday and Wednesday is to then
        # the day should not be changed.
        #     Wednesday - Wednesday = 2 - 2 = 0
        # If from is Tuesday and Friday is to then
        # the day should be increased by 3
        #     Friday - Tuesday = 4 - 1 = 3
        days = to_weekday - from_weekday
    else:
        # If from is Friday and Monday is to then the
        # day should be increased by 3.
        #    7 - Friday + Monday = 7 - 4 + 0 = 3 
        # If from is Thursday and Tuesday is to then the
        # day should be increased by 5.
        #    7 - Thursday + Tuesday = 7 - 3 + 1 = 5
        days = 7 - from_weekday + to_weekday

    return days

def get_time(time_str):
    return datetime.datetime.strptime(time_str, '%H:%M').time()

module = AcmBotModule
