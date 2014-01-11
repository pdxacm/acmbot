#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
import urllib
from StringIO import StringIO
from kitnirc.modular import Module
from bs4 import BeautifulSoup
 
_log = logging.getLogger(__name__)

ACM_BASE_URL = 'http://acm.pdx.edu'

parser_output = StringIO()

class ArgumentParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        super(ArgumentParser, self)._print_message(message, parser_output)
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, None)

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')
subparser_events = subparsers.add_parser('!events')

def reset_parser_output():
    parser_output.seek(0, 0)
    parser_output.truncate()

class AcmBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def messages(self, client, actor, recipient, message):
        # Only pay attention if addressed directly in channels
        try:
            args = parser.parse_args(message.split())
        except (NameError, TypeError):
            _log.debug("message not reconized %r", message)
            reset_parser_output()
            return

        if parser_output.getvalue():
            parser_output.seek(0, 0)
            parser_output.truncate()
            return
            
        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", actor, recipient)
        
        if args.subparser == "!events":
            
            html = urllib.urlopen(ACM_BASE_URL + '/events.php').read()
            soup = BeautifulSoup(html)
            messages = [
                soup.ui.text.replace('\n', '').strip(),
                ACM_BASE_URL + soup.ui.a['href'],
            ]
            for message in messages:
                client.reply(recipient, actor, message)
                reset_parser_output()

        # Stop any other modules from handling this message.
        return True

module = AcmBotModule
