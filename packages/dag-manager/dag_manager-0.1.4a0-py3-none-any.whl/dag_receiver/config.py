# -*- coding: utf-8 -*-
# @Time    : 2019-04-16 11:56
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: config.py
# @Software: PyCharm
import os
from dag_receiver.exceptions import DagReceiverException

# DAG_FOLDER = '/user/local/airflow/dags'
DAG_FOLDER = os.getenv('AIRFLOW_DAG_FOLDER')

if DAG_FOLDER is None:
    raise DagReceiverException('environment variable AIRFLOW_DAG_FOLDER not found')
