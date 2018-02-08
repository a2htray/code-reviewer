# -*- coding:utf-8 -*-


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

    def check(self):
        pass

    def __str__(self):

        desc = "Name: " + self.name + "\n"
        desc += "Git Url: " + self.git_url + "\n"
        desc += "Members: " + "; ".join(self.members) + "\n"
        desc += "File System: " + self.sys_path

        return desc
