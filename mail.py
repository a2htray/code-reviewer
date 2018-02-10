#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Mail Model"""


class Mail:
    SERVER = None

    def send(self, _from, to, subject, content):
        header = "From: " + _from + "\n"
        header += "To: " + to + "\n"
        header += "Subject: " + subject + "\n"
        header += "\n"
        header += content

        self.SERVER.sendmail(_from, to, header)

    def set_server(self, server):
        self.SERVER = server

