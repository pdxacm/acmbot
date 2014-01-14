#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
import urllib
from StringIO import StringIO
from kitnirc.modular import Module
from bs4 import BeautifulSoup
from botparse import BotParse
 
_log = logging.getLogger(__name__)

ACM_EVENTS_YAML = 'https://raw2.github.com/pdxacm/acm.pdx.edu/master/files/events.yaml'
ACM_BASE_URL = 'http://acm.pdx.edu'

parser_output = StringIO()

parser = BotParse()
command_events = parser.add_command('!events')

def reset_parser_output():
    parser_output.seek(0, 0)
    parser_output.truncate()

class AcmBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def messages(self, client, actor, recipient, message):

        self.client = client
        self.actor = actor
        self.recipient = recipient
        self.message = message

        # Only pay attention if addressed directly in channels
        try:
            args = parser.parse_args(self.message.split())
        except (NameError, TypeError):
            _log.debug("message not reconized %r", self.message)
            reset_parser_output()
            return

        if parser_output.getvalue():
            parser_output.seek(0, 0)
            parser_output.truncate()
            return
            
        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", self.actor, self.recipient)
        
        if args.command == "!events":
            if args.help:
                messages = command_events.format_help().split('\n')
            else:
                html = urllib.urlopen(ACM_BASE_URL + '/events.php').read()
                soup = BeautifulSoup(html)
                messages = [
                    soup.ui.text.replace('\n', '').strip(),
                    ACM_BASE_URL + soup.ui.a['href'],
                ]
        elif args.command == "!help":
            messages = parser.format_help().split('\n')

        for message in messages:
            self.client.reply(self.recipient, self.actor, message)
            reset_parser_output()

        # Stop any other modules from handling this message.
        return True
    
module = AcmBotModule
