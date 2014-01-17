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
            args = parser.parse_args(self.message.split())
        except (NameError, TypeError):
            _log.debug("message not reconized %r", self.message)
            return

        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", self.actor, self.recipient)
        
        if args.command == "!events":
            if args.help:
                messages = command_events.format_help().split('\n')
            else:
                if not config.has_section("acmbot"):
                    _log.info("No config section for acmbot")
                    return
                if config.has_option("acmbot", "base_url"):
                    base_url = config.get("acmbot", "base_url")
                else:
                    return
                def get_date(entry):
                    return datetime.datetime.strptime(
                        entry['date'],
                        '%m-%d-%Y',
                    ).date()
                messages = []
                events_html = urllib.urlopen(
                    '{}/files/events.yaml'.format(base_url)
                ).read()
                events = yaml.load(events_html)
                sorted_events = sorted(events, key=get_date, reverse=True)
                current_events = takewhile(
                    lambda x: get_date(x) >= datetime.date.today(),
                    sorted_events,
                )
                for i, event in enumerate(current_events):
                    messages.append(event['title'])
                    messages.append('{}/event.php?event={}'.format(
                        base_url, str(len(events) - i - 1),
                    ))
        elif args.command == "!help":
            messages = parser.format_help().split('\n')

        for message in messages:
            self.client.reply(self.recipient, self.actor, message)

        # Stop any other modules from handling this message.
        return True
    
module = AcmBotModule
