# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 16:02
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: config.py
# @Software: PyCharm
import os
import configparser

from dag_manager.exceptions import DagManagerException


dag_manager_home = os.getenv('DAG_MANAGER_HOME')
if dag_manager_home is None:
    raise DagManagerException('environment variable DAG_MANAGER_HOME not found')

filename = os.path.join(dag_manager_home, 'dag_manager.cfg')
if not os.path.exists(filename) or os.path.isdir(filename):
    raise DagManagerException('{} not found'.format(filename))

conf = configparser.ConfigParser()
conf.read(filename)

REDIS_CONFIG = {
    'host': conf.get('redis', 'host'),
    'port': conf.getint('redis', 'port'),
    'db': conf.getint('redis', 'db'),
}

ALL_DAGS_ZIP_NAME = conf.get('core', 'all_dags_zip_name')
DAG_FOLDER = conf.get('core', 'dag_folder')
ALL_DAGS_ZIP_PATH = os.path.join(DAG_FOLDER, ALL_DAGS_ZIP_NAME)

ACCEPTED_EXT = ('.zip', '.py')

REDIS_PREFIX = 'D_M_PREFIX_'
REDIS_KEYS = {
    'lock_modification': REDIS_PREFIX + '___LocK_mODiFY__',
    'all_dag_ids': REDIS_PREFIX + '___dAgS___',
    'last_update_time': REDIS_PREFIX + '__lAsT_UpdAte_TiMe__',
    'last_zip_time': REDIS_PREFIX + '__lAsT_zIP_TiMe__',
}

# 需同步更新的节点
SYNC_URLS = conf.get('receiver', 'urls').split(',')
