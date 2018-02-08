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

exit(-1)

def process_commits():
    cmd = "cd ../" + project.name + "&& git log --all --since=" + str(no_days) + ".day --name-status"
    response = lib.execute_cmd(cmd)

    commit_id = ''
    author = ''
    date = ''

    for line in response.splitlines():
        # commit id
        if line.startswith("commit"):
            if commit_id != "":
                project.commits.append(Commit(_id=commit_id, git_url=project.git_url, author=author, date=date))

            author = ''
            date = ''
            commit_id = line[7:]
        # author
        if line.startswith("Author"):
            if re.search('\<(.*?)\>', line):
                author = re.search('\<(.*?)\>', line).group(1)

        # date
        if line.startswith("Date"):
            date = line[5:]

    if commit_id != "":
        project.commits.append(Commit(_id=commit_id, git_url=project.git_url, author=author, date=date))

    return commits


def select_reviewer(author, group):
    if author in group:
        group.remove(author)

    print group

    reviewer = random.choice(group)

    return reviewer


def format_review_commit(commit):
    review_req = ""
    review_req += "URL:" + project_url + "/commit/" + commit.id + "\n"
    review_req += "Author:" + commit.author + "\n"
    review_req += "Date:" + commit.date + "\n"

    return review_req


FROM_EMAIL, FROM_PWD, SERVER, PORT = lib.get_email_config(config)


def send_email(to, subject, body):
    header = "From: " + FROM_EMAIL + "\n"
    header += "To: " + to + "\n"
    header += "Subject: " + subject + "\n"
    header += "\n"
    header += body

    print "** Sending email to " + to

    mail_server = smtplib.SMTP(SERVER, PORT)
    mail_server.login(FROM_EMAIL, FROM_PWD)
    mail_server.sendmail(FROM_EMAIL, to, header)
    mail_server.quit()


def scheduler_review_request(commits):
    date = time.strftime("%Y-%m-%d")

    for commit in commits:
        reviewer = select_reviewer(commit.author, project_members)
        print project_members
        subject = date + " Code Review [commit id:" + commit.id + "]"
        body = "Hello " + reviewer + " you have been selected to review the code for commit\n"
        body += "done by " + commit.author + ".\n"
        body += "\n"

        body += format_review_commit(commit)

        send_email(reviewer, subject, body)



if os.path.isdir("../" + project):
    print lib.execute_cmd("cd " + "../" + project + "&& git pull")
else:
    print lib.execute_cmd("git clone " + project_url + " ../" + project)

print "***Done ****"

print "Processing the scheduler against project " + project + " ..."

commits = process_commits()

scheduler_review_request(commits)


