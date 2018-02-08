#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from abc import ABCMeta, abstractmethod


class CommandLeader(object):
    def __init__(self):
        self.commands = []

    def clear(self):
        self.commands = []
        return self

    def add_command(self, command):
        assert type(command) == Command
        if isinstance(command, Command):
            print 1
            self.commands.append(command)
        elif isinstance(command, list):
            print 2
            self.commands += self.commands

        return self

    def _get_commands(self):

        return ' && '.join(self.commands)

    def execute(self):

        resp = os.popen(self._get_commands()).read()

        return resp


class Command(object):
    __class__ = ABCMeta

    @abstractmethod
    def get_cmd(self):
        pass


class CdCommand(Command):

    CMD = 'cd'

    def __init__(self, path):
        self.path = path

    def get_cmd(self):
        return self.CMD + ' ' + self.path


class GitPullCommand(Command):

    CMD = 'git pull'

    def get_cmd(self):
        return self.CMD


class GitCloneCommand(Command):
    CMD = 'git clone'

    def __init__(self, git_url, alias_path):
        self.git_url = git_url
        self.alias_path = alias_path

    def get_cmd(self):
        return self.CMD + ' ' + self.git_url + ' ' + self.alias_path

command_leader = CommandLeader()