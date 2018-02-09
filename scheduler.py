# -*- coding:utf-8 -*-

import argparse
import json
import os
import re
import random
import time
import smtplib

import lib

from commit import Commit
from project import Project
from command import command_leader
from mail import Mail

parser = argparse.ArgumentParser(description="Code Review Scheduler Program")
parser.add_argument("-n", nargs="?", type=int, default=1, help="Number of days to look for log.")
parser.add_argument("-p", nargs="?", type=str, default="em", help="Project name.")
parser.add_argument("-d", nargs="?", type=str, default='.', help="Project dictionary base on")
parser.add_argument("-a", nargs="?", type=str, default=None, help="Alias project name")

args = parser.parse_args()

no_days = args.n
p = args.p
project_url = None
project_members = None
sys_project_name = args.a if args.a else p

config = lib.make('cfgparser', file_path='./config.json').load()
printer = lib.make('printer')

printer.display("Processing the scheduler against project " + p + " ...")


def current_project(name):
    for p in config.get('projects'):
        if p['name'] == name:
            git_url = p['git_url']
            members = p['members']

            return Project(name=name, git_url=git_url, members=members, sys_path='/'.join([args.d, sys_project_name]))


project = current_project(p)

printer.display("******** Doing project checkout *********")
project.update()
project.get_commits(no_days, True)

# configuration for mail, and create an mail instance
FROM_EMAIL, FROM_PWD, SERVER, PORT = lib.get_email_config(config)
mail_server = smtplib.SMTP(SERVER, PORT)
mail_server.login(FROM_EMAIL, FROM_PWD)
mail = Mail()
mail.set_server(mail_server)


def select_reviewer(author, group):
    if author in group:
        group.remove(author)
    reviewer = random.choice(group)

    return reviewer


printer.display('Processing the scheduler against project " + project + " ...')
date = time.strftime("%Y-%m-%d")

for commit in project.commits:
    reviewer = select_reviewer(commit.author, project.members)

    subject = date + " Code Review [commit id:" + commit.id + "]"
    body = "Hello " + reviewer + " you have been selected to review the code for commit\n"
    body += "done by " + commit.author + ".\n"
    body += "\n"

    printer.display('send email to ' + reviewer)
    mail.send(_from=FROM_EMAIL, to=reviewer, subject=subject, content=body + commit.format())

printer.display('***Done ****')



