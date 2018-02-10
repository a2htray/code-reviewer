#!/usr/bin/python
# -*- coding:utf-8 -*-

"""alias for the specific class"""

import cfgparser
import printer

__ALIAS__ = {
    'cfgparser': cfgparser.JsonParser,
    'printer': printer.ShellPrinter
}
