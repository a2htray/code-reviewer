# -*- coding:utf-8 -*-

import os
from command import command_leader, CdCommand, GitPullCommand, GitCloneCommand

class Project(object):

    def __init__(self, name, git_url, members, sys_path):
        self.name = name
        self.git_url = git_url
        self.members = members
        self.sys_path = sys_path

        self.commits = {}

    def add_commit(self, commit):
        self.commits[commit.id] = commit

    def batch_add_commits(self, commits):
        for commit in commits:
            self.add_commit(commit)

    def update(self):
        command_leader.clear()

        if os.path.isdir(self.sys_path):
            resp = command_leader.add_command([
                CdCommand(self.sys_path),
                GitPullCommand()
            ]).execute()
        else:
            resp = command_leader.add_command(GitCloneCommand(
                git_url=self.git_url,
                alias_path=self.sys_path
            )).execute()
        print resp
        return resp

    def __str__(self):

        desc = "Name: " + self.name + "\n"
        desc += "Git Url: " + self.git_url + "\n"
        desc += "Members: " + "; ".join(self.members) + "\n"
        desc += "File System: " + self.sys_path

        return desc
