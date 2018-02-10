#!/usr/bin/python
# -*- coding:utf-8 -*-

"""outputs definition, such as shell standard output"""


from abc import ABCMeta, abstractmethod


class Printer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def display(self, str):
        pass


class ShellPrinter(Printer):
    def display(self, _str):
        print _str