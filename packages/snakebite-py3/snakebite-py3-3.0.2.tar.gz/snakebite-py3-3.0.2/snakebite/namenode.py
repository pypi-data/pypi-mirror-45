# -*- coding: utf-8 -*-
# Copyright (c) 2013 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# python 3 support
from __future__ import absolute_import, print_function, division

class Namenode(object):
    '''Namenode class - represents HDFS namenode'''
    DEFAULT_PORT = 8020
    DEFAULT_VERSION = 9

    def __init__(self, host, port=DEFAULT_PORT, version=DEFAULT_VERSION):
        self.host = host
        self.port = port
        self.version = version

    def is_active(self):
        return True

    def toDict(self):
        return {"namenode": self.host,
                "port": self.port,
                "version": self.version}
