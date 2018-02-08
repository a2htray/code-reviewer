# -*- coding:utf-8 -*-


class Commit:

    def __init__(self, _id, git_url, author, date):
        self.id = _id
        self.git_url = git_url
        self.author = author
        self.date = date

    def format(self):
        review_req = ""
        review_req += "URL:" + self.git_url + "/commit/" + self.id + "\n"
        review_req += "Author:" + self.author + "\n"
        review_req += "Date:" + self.date + "\n"

        return review_req
