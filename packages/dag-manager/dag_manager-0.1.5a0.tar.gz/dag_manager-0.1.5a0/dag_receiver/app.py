# -*- coding: utf-8 -*-
# @Time    : 2019-04-16 11:40
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: app.py
# @Software: PyCharm
import os
import shutil
from zipfile import ZipFile

from flask import Flask, request

from dag_receiver.config import DAG_FOLDER

app = Flask(__name__)


@app.route('/<dag_id>/<op>', methods=['POST'])
def index(dag_id, op):
    path = os.path.join(DAG_FOLDER, dag_id)
    print(path)
    if op == 'DELETE':
        if not os.path.exists(path) or not os.path.isdir(path):
            return 'dag[{}] not found'.format(dag_id), 500
        shutil.rmtree(path)
    else:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        file = request.files['file']
        print(file)
        file_path = os.path.join(path, file.filename)
        file.save(file_path)
        if file_path.endswith('.zip'):
            with ZipFile(file_path) as zf:
                zf.extractall(path)
            os.remove(file_path)
    return 'ok'


@app.route('/echo')
def echo():
    return 'ok'


if __name__ == '__main__':
    app.run()
