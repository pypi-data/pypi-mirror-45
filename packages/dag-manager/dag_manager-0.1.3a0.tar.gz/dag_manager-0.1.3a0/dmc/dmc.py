# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 17:33
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: cli.py
# @Software: PyCharm
import json
import os
import shutil
from zipfile import ZipFile

import requests


class DagManagerException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class DMCParametersException(DagManagerException):
    pass


class DagManagerClient(object):
    __slots__ = ['base_url', 'folder']

    def __init__(self, base_url, folder):
        self.base_url = base_url
        self.folder = folder

    def get(self, dag_id=None):
        """
        从DagManager拉取指定的dag，dag_id为None时，拉取所有dag。
        会建一个和dag_id同名的文件夹存放dag文件，对于zip文件，会解压，并删除zip文件
        拉取指定dag，会先删除指定dag
        拉取所有dag时，会先删除所有dag
        :param dag_id:
        :return:
        """
        url = os.path.join(self.base_url, 'dags', dag_id or '')
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DagManagerException(resp.text)
        d = os.path.join(self.folder, dag_id or '')
        # 拉取所有dag时，需先删除目前的所有的dag
        if dag_id is None:
            self._clear_folder()
        else:
            if os.path.exists(d):
                shutil.rmtree(d)
            os.mkdir(d)
        path = os.path.join(d, os.path.basename(resp.request.path_url))
        with open(path, 'wb') as f:
            f.write(resp.content)
        if resp.headers['Content-Type'] == 'application/zip':
            with ZipFile(path) as zf:
                zf.extractall(d)
            os.remove(path)
        # 拉取所有dag时，将解压后的所有文件放置在{self.folder}/{dag_id}/{dag_id}.[py|zip]
        # 对于zip的dag，还需要解压，并删除zip文件
        if dag_id is None:
            for filename in os.listdir(self.folder):
                old_path = os.path.join(self.folder, filename)
                new_dir = os.path.join(self.folder, os.path.splitext(filename)[0])
                new_path = os.path.join(new_dir, filename)
                os.mkdir(new_dir)
                os.rename(old_path, new_path)
                if filename.endswith('.zip'):
                    with ZipFile(new_path) as zf:
                        zf.extractall(new_dir)
                    os.remove(new_path)

    def _clear_folder(self):
        for d in os.listdir(self.folder):
            path = os.path.join(self.folder, d)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def remove(self, dag_id):
        path = os.path.join(self.folder, dag_id)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        url = os.path.join(self.base_url, 'dags', dag_id or '')
        resp = requests.delete(url)
        if resp.status_code != 200:
            raise DagManagerException(resp.text)

    def clear(self):
        self._clear_folder()

    def list(self, pattern=None):
        url = os.path.join(self.base_url, 'dag_ids', pattern or '*')
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DagManagerException(resp.text)
        dags = json.loads(resp.text)
        return sorted(dags)

    def upload(self, dag_id, filename, dag_path=None):
        url = os.path.join(self.base_url, 'dags', dag_id or '')
        files = {'file': open(filename, 'rb')}
        _, ext = os.path.splitext(filename)
        data = {}
        if ext == '.zip':
            if dag_path is None:
                raise DMCParametersException('must specify dag_path, when upload a zip file')
            data = {'dag_path': dag_path}
        resp = requests.post(url, files=files, data=data)
        if resp.status_code != 200:
            raise DagManagerException(resp.text)
