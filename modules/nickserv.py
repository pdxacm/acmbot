#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging

from kitnirc.modular import Module

_log = logging.getLogger(__name__)

class NickServModule(Module):
    """A KitnIRC module which automatically authenticates
    nicks via NickServ """
    
    @Module.handle("WELCOME")
    def register_nick(self, client, hostmask):

        _log.info("Beginning automatic nick configuration...")
        
        config = self.controller.config

        if not config.has_section("nickserv"):
            _log.info("No password found for nickserv.")
            return

        if config.has_option("nickserv", "password"):
            password = config.get("nickserv", "password")
            client.msg("NickServ", "IDENTIFY {}".format(password))
        else:
            _log.info("No password found for nickserv.")

        _log.info("Automatic nick configuration complete.")

module = NickServModule
