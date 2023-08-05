# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 16:02
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: config.py
# @Software: PyCharm
import os

REDIS_CONFIG = {
    'host': 'bj-cpu008.aibee.cn',
    'port': 26379,
    'db': 3,
}


ALL_DAGS_ZIP_NAME = 'all_dags.zip'
DAG_FOLDER = 'app/static'
ALL_DAGS_ZIP_PATH = os.path.join(DAG_FOLDER, ALL_DAGS_ZIP_NAME)
ACCEPTED_EXT = ('.zip', '.py')
REDIS_PREFIX = 'D_M_PREFIX_'
REDIS_KEYS = {
    'lock_modification': REDIS_PREFIX + '___LocK_mODiFY__',
    'all_dag_ids': REDIS_PREFIX + '___dAgS___',
    'last_update_time': REDIS_PREFIX + '__lAsT_UpdAte_TiMe__',
    'last_zip_time': REDIS_PREFIX + '__lAsT_zIP_TiMe__',
}
# REDIS_ADD_DAGS = REDIS_PREFIX + '___AdD___dAgS___'
# REDIS_UPDATE_DAGS = REDIS_PREFIX + '___uPdAtE___dAgS___'
# REDIS_REMOVE_DAGS = REDIS_PREFIX + '___ReMoVe___dAgS___'


# 需同步更新的节点
SYNC_URLS = [
    "http://localhost:5001/{dag_id}/{op}"
]