#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
from StringIO import StringIO
from kitnirc.modular import Module

_log = logging.getLogger(__name__)

parser_output = StringIO()

class ArgumentParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        super(ArgumentParser, self)._print_message(message, parser_output)
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, None)

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')
subparser_product = subparsers.add_parser('!events')

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
            
            message = "todo"

            # The 'reply' function automatically sends a replying PM if
            # the bot was PM'd, or addresses the user in a channel who
            # addressed the bot in a channel.
            client.reply(recipient, actor, message)
            
            reset_parser_output()

        # Stop any other modules from handling this message.
        return True

module = AcmBotModule
