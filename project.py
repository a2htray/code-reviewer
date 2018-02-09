# -*- coding:utf-8 -*-

import os
import re

from command import command_leader, CdCommand, GitPullCommand, GitCloneCommand, GitLogCommand
from commit import Commit


class Project(object):
    def __init__(self, name, git_url, members, sys_path):
        self.name = name
        self.git_url = git_url
        self.members = members
        self.sys_path = sys_path
        self.commits = []

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

        return resp

    def get_commits(self, since=5, with_name_status=True):
        command_leader.clear()

        resp = command_leader.add_command([
            CdCommand(self.sys_path),
            GitLogCommand(since, with_name_status)
        ]).execute()

        self._process_commits(resp)


    def _process_commits(self, resp):
        """
            this is an important method
        """
        commit_id = ''
        author = ''
        date = ''

        for line in resp.splitlines():
            # commit id
            if line.startswith("commit"):
                if commit_id != "":
                    self.commits.append(Commit(_id=commit_id, git_url=self.git_url, author=author, date=date))

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
            self.commits.append(Commit(_id=commit_id, git_url=self.git_url, author=author, date=date))

    def __str__(self):
        desc = "Name: " + self.name + "\n"
        desc += "Git Url: " + self.git_url + "\n"
        desc += "Members: " + "; ".join(self.members) + "\n"
        desc += "File System: " + self.sys_path

        return desc

