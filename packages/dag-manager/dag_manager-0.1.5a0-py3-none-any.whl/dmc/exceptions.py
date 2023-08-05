# -*- coding: utf-8 -*-
# @Time    : 2019-04-16 14:42
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: exceptions.py
# @Software: PyCharm


class DMCException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class DMCParametersException(DMCException):
    pass
