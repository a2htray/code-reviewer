# -*- coding:utf-8 -*-

import os
import alias


def make(_class, *args, **kwargs):
    return alias.__ALIAS__[_class](*args, **kwargs)


def execute_cmd(cmd):
    print "**** Executing command `" + cmd + "`****"
    response = os.popen(cmd).read()

    return response

def get_email_config(config):
    return config.get('email.address'), config.get('email.password'), config.get('email.server'), config.get(
        'email.port')


