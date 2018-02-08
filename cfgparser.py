# -*- coding:utf-8 -*-

import os
import json

from abc import ABCMeta, abstractmethod


class CfgParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self):
        pass


class JsonParser(CfgParser):

    main_config = None

    def __init__(self, file_path):

        # the file path must be exist
        assert os.path.isfile(file_path)

        self.file_path = file_path

    def load(self):
        with open(self.file_path) as cfg_file:
            self.main_config = json.load(cfg_file)
        print self.main_config
        # the variant mustn't be None
        assert self.main_config

        return self

    def get(self, key):
        if "." in key:
            keys = key.split(".")

            def _read(keys, obj):
                if len(keys) == 1:
                    return obj[keys[0]]

                return _read(keys[1:], obj[keys[0]])

            return _read(keys, self.main_config)

        else:
            return self.main_config[key]




