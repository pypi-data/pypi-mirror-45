# -*- coding: utf-8 -*-
# @Time    : 2019-04-09 15:02
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: app.py
# @Software: PyCharm
import functools
import logging
import os
import shutil
import uuid
import zipfile
from datetime import datetime
from enum import Enum

import requests
from airflow.models import DAG
from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

from dag_manager.app.auth import need_auth
from dag_manager.app.config import (
    ALL_DAGS_ZIP_NAME,
    DAG_FOLDER,
    ALL_DAGS_ZIP_PATH,
    ACCEPTED_EXT,
    REDIS_KEYS,
    SYNC_URLS,
)
from dag_manager.app.globals import get_redis_client
from dag_manager.app.util.lock import unlock, try_lock


class OP(Enum):
    ADD = 'ADD'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'


dags_blueprint = Blueprint('dags', __name__, url_prefix='/dags')


def not_zipping(func):
    """
    该装饰器，用以判断是否
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = REDIS_KEYS['lock_modification']
        if not try_lock(key):
            return 'dag modification locked now, please modify dag later.', 500
        result = func(*args, **kwargs)
        unlock(key)
        return result

    return wrapper


def last_update_time():
    return float(get_redis_client().get(REDIS_KEYS['last_update_time']) or 0)


def last_zip_time():
    return float(get_redis_client().get(REDIS_KEYS['last_zip_time']) or 0)


def set_last_update_time(time):
    get_redis_client().set(REDIS_KEYS['last_update_time'], time)


def set_last_zip_time(time):
    get_redis_client().set(REDIS_KEYS['last_zip_time'], time)


@dags_blueprint.route('/')
@need_auth
@not_zipping
def get_all_dags():
    if last_zip_time() < last_update_time() or not os.path.exists(ALL_DAGS_ZIP_PATH):
        zip_dags()
    return redirect(url_for('static', filename='all_dags.zip'))


@dags_blueprint.route('/<dag_id>')
@need_auth
@not_zipping
def get(dag_id):
    cur = find_dag(dag_id)
    if cur is None:
        return '{dag_id}.py or {dag_id}.zip not found'.format(dag_id=dag_id), 500
    return redirect(url_for('static', filename=os.path.basename(cur)))


@dags_blueprint.route('/<dag_id>', methods=['DELETE'])
@need_auth
@not_zipping
def delete(dag_id):
    cur = find_dag(dag_id)
    if cur is None:
        return '{dag_id}.py or {dag_id}.zip not found'.format(dag_id=dag_id)
    os.remove(cur)
    set_last_update_time(datetime.utcnow().timestamp())
    replicate(cur, dag_id, OP.DELETE)
    get_redis_client().srem(REDIS_KEYS['all_dag_ids'], dag_id)
    return 'done'


@dags_blueprint.route('/<dag_id>', methods=['POST'])
@need_auth
@not_zipping
def post(dag_id):
    """
    可上传的dag分为两类，1）单个py文件 2）包含依赖的zip文件，后者需要使用dag_path指定dag文件的路径
    todo 对zip是否需要更严格检查
    :param dag_id:
    :return:
    """
    file = request.files['file']
    _, ext = os.path.splitext(file.filename)
    if ext not in ACCEPTED_EXT:
        return 'not accept ext: {}'.format(ext), 500
    # 将文件存储在临时目录/tmp，并在其中检查Dag文件是否合法
    tmp_path = os.path.join('/tmp', secure_filename(file.filename))
    file.save(tmp_path)
    dag_path = request.form.get('dag_path')
    print('dag_path', dag_path)
    ok, reason = is_valid_dag_file(dag_id, tmp_path, ext, dag_path)
    if not ok:
        return reason, 500
    else:
        # 如果dag文件合法，则
        # 1）若dag已存在，先删除
        # 2）将文件从临时目录移动到 os.path.join(DAG_FOLDER, dag_id + ext)
        # 3）将更新同步至airflow scheduler、webserver结点
        # 4）记录更新时间
        # 5）将dag_id加入redis集合中
        # todo 保持操作atomic
        cur = find_dag(dag_id)
        if cur is not None:
            os.remove(cur)
        real_path = os.path.join(DAG_FOLDER, dag_id + ext)
        os.rename(tmp_path, real_path)
        replicate(real_path, dag_id, OP.UPDATE if get_redis_client().sismember(REDIS_KEYS['all_dag_ids'], dag_id) else OP.ADD)
        set_last_update_time(datetime.utcnow().timestamp())
        get_redis_client().sadd(REDIS_KEYS['all_dag_ids'], dag_id)
        return 'ok'


def zip_dags():
    with zipfile.ZipFile(ALL_DAGS_ZIP_PATH, mode='w') as zf:
        for f in os.listdir(DAG_FOLDER):
            if os.path.isfile(os.path.join(DAG_FOLDER, f)) and os.path.splitext(f)[1] in ACCEPTED_EXT and f != ALL_DAGS_ZIP_NAME:
                zf.write(os.path.join(DAG_FOLDER, f), f)
    set_last_zip_time(datetime.utcnow().timestamp())


def find_dag(dag_id):
    path = os.path.join(DAG_FOLDER, dag_id + '.py')
    if os.path.exists(path):
        return path
    path = os.path.join(DAG_FOLDER, dag_id + '.zip')
    if os.path.exists(path):
        return path
    return None


def is_valid_dag_file(dag_id, path, ext, dag_path=None):
    """
    合法需要符合以下条件：
    1、对于py文件，其包含一个模块级的Dag对象，且id与dag_id一样
    2、对于zip文件夹，仅检查dag_path指定的py文件，其包含一个模块级的Dag对象，且id与dag_id一样，且dag_path的文件名（除后缀）与dag_id一样
    # todo 更严格检查解压后的zip文件夹
    :param dag_id: dag_id
    :param path: 文件或者文件夹路径
    :param dag_path:
    :param ext: 后缀名
    :return: (is_valid, reason)
    """
    from importlib import util
    dag = None
    module_name = '_' + str(uuid.uuid1()).replace('-', '_')
    if ext == '.zip':
        if dag_path is None:
            return False, 'must specify dag_path where upload a zip file'
        zip_tract_path = tract_zip(path)
        path = os.path.join(zip_tract_path, dag_path)
    try:
        spec = util.spec_from_file_location(module_name, path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if ext == '.zip':
            shutil.rmtree(zip_tract_path)
    except Exception:
        return False, 'load dag exception'
    for v in dir(mod):
        if isinstance(getattr(mod, v), DAG):
            if dag is not None:
                return False, 'there are more than one dags'
            dag = getattr(mod, v)
    if dag is None:
        return False, 'dag named "{}" not found'.format(dag_id)
    if dag.dag_id != dag_id or \
            (ext == '.zip' and dag_id != os.path.basename(os.path.splitext(dag_path)[0])):
        return False, 'incorrect dag_id'
    return True, 'ok'


def tract_zip(filename):
    """
    将zip文件解压至/tmp/{uuid}中
    :param filename: 待解压文件名
    :return: /tmp/{uuid}
    """
    p = os.path.join('/tmp', str(uuid.uuid1()))
    with zipfile.ZipFile(filename) as zf:
        zf.extractall(p)
    return p


def replicate(path, dag_id, op):
    """
    将dag的更新复制给同步结点
    :param path: 文件路径
    :param dag_id:
    :param op: OP object
    :return:
    """
    files = {'file': open(path, 'rb')} if op is not OP.DELETE else None
    for item in SYNC_URLS:
        url = item.format(dag_id=dag_id, op=op.value)
        try:
            resp = requests.post(url, files=files, timeout=5)
            if resp.status_code != 200:
                logging.error('replicate {} failed, return: {} - {}', url, resp.status_code, resp.text)
                # todo 此处需要报警，并且考虑是否需要进一步的错误处理，例如回滚
        except Exception:
            logging.error('replicate {} failed, return: {} - {}', url, resp.status_code, resp.text)
            # todo 此处需要报警，并且考虑是否需要进一步的错误处理，例如回滚
    pass
