# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 15:05
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: lock.py
# @Software: PyCharm
"""
实现分布式锁
"""
import functools
import time

from dag_manager.globals import get_redis_client


def try_lock(key):
    ok = get_redis_client().setnx(key, 1) == 1
    get_redis_client().expire(key, 600)
    return ok


def lock(key):
    while get_redis_client().setnx(key, 1) == 0:
        print('lock failed')
        time.sleep(0.2)
    get_redis_client().expire(key, 600)


def unlock(key):
    get_redis_client().delete(key)


def locking(key):
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock(key)
            result = func(*args, **kwargs)
            unlock(key)
            return result
        return wrapper
    return outer
