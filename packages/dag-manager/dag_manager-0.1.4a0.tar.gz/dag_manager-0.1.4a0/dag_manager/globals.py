# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 19:32
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: globals.py
# @Software: PyCharm
import redis

from dag_manager.config import REDIS_CONFIG

conn_pool = redis.ConnectionPool(max_connections=128, retry_on_timeout=True, socket_keepalive=True, **REDIS_CONFIG)


def get_redis_client():
    return redis.Redis(connection_pool=conn_pool)
