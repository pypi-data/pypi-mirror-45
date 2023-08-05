# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 16:19
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: test.py
# @Software: PyCharm
import requests
import os
import uuid
from zipfile import ZipFile

from dag_manager.app.util.lock import locking
from dag_manager.app.config import REDIS_KEYS
from dag_manager.app.globals import get_redis_client
from dmc.dmc import DagManagerClient


@locking('xxx')
def test():
    pass


# 测试/dags接口
def test_dags():
    manager_dag_folder = "/Users/wutong/work/py/dag_manager/app/static"
    node_dag_folder = "/Users/wutong/work/py/replication/static"
    test_dag_folder = "/Users/wutong/work/py/dag_manager/tests/dags"
    base_url = 'http://localhost:5000/dags/'
    all_zip_path = os.path.join(manager_dag_folder, 'all_dags.zip')

    for key in REDIS_KEYS.values():
        get_redis_client().delete(key)
    if os.path.exists(all_zip_path):
        os.remove(all_zip_path)

    files = ['example_bash_operator.py', 'example_python_operator.py', 'example_xcom.zip']
    dag_ids = ['example_bash_operator', 'example_python_operator', 'example_xcom']
    for f, dag_id in zip(files, dag_ids):
        path = os.path.join(test_dag_folder, f)
        if dag_id != 'example_xcom':
            resp = requests.post(base_url + dag_id, files={'file': open(path, 'rb')})
        else:
            resp = requests.post(base_url + dag_id, files={'file': open(path, 'rb')}, data={'dag_path': 'example_xcom.py'})
        if resp.status_code != 200:
            print(resp.text)
        resp = requests.get(base_url + dag_id)
        if resp.status_code != 200:
            raise Exception("get {} failed".format(base_url + dag_id))
        with open(path, 'rb') as ff:
            if ff.read() != resp.content:
                raise Exception("content in file is different from http body")

    if set(os.listdir(manager_dag_folder)) != set(files):
        raise Exception("manager_dag_folder: " + str(os.listdir(manager_dag_folder)))
    if set(os.listdir(node_dag_folder)) != set(dag_ids):
        raise Exception("node_dag_folder: " + str(os.listdir(node_dag_folder)))

    resp = requests.get(base_url)
    tmp_path = os.path.join("/tmp", str(uuid.uuid1()))
    os.mkdir(tmp_path)
    filename = os.path.join(tmp_path, 'all_dags.zip')
    with open(filename, 'wb') as ff:
        ff.write(resp.content)
    with ZipFile(filename) as zf:
        zf.extractall(tmp_path)
    os.remove(filename)

    for ff in os.listdir(tmp_path):
        old_file_name = os.path.join(tmp_path, ff)
        new_file_name = os.path.join(test_dag_folder, ff)
        with open(old_file_name, 'rb') as f1:
            with open(new_file_name, 'rb') as f2:
                if f1.read() != f2.read():
                    raise Exception("{} is different from {}".format(old_file_name, new_file_name))

    for f, dag_id in zip(files, dag_ids):
        requests.delete(base_url + dag_id)
    if set(os.listdir(node_dag_folder)) != set():
        raise Exception("node_dag_folder is not empty")


if __name__ == '__main__':
    test_dags()
    dmc = DagManagerClient('http://localhost:5000', '/Users/wutong/work/py/dag_manager/tests/dmc')
    dmc.upload('example_bash_operator', '/Users/wutong/work/py/dag_manager/tests/dags/example_bash_operator.py')
    dmc.upload('example_python_operator', '/Users/wutong/work/py/dag_manager/tests/dags/example_python_operator.py')
    dmc.upload('example_xcom', '/Users/wutong/work/py/dag_manager/tests/dags/example_xcom.zip')

    dmc.get()
    # dmc.get('example_bash_operator')
    print(dmc.list())
    print(dmc.list('*bash*'))

    # dmc.clear()
    # dmc.delete('example_xcom')