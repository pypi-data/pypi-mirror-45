# -*- coding: utf-8 -*-
# @Time    : 2019-04-16 14:28
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: exceptions.py
# @Software: PyCharm


class DagManagerException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason
