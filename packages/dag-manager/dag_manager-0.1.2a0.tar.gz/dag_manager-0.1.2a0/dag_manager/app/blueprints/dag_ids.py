# -*- coding: utf-8 -*-
# @Time    : 2019-04-11 18:05
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: dag_ids.py
# @Software: PyCharm
import json
import re

from flask import Blueprint

from dag_manager.app.config import (
    REDIS_KEYS,
)
from dag_manager.app.globals import get_redis_client

dag_ids_blueprint = Blueprint('dag_ids', __name__, url_prefix='/dag_ids')


@dag_ids_blueprint.route('/<pattern>')
def get(pattern):
    if re.match(r'^[A-Za-z_*][A-Za-z0-9_\*]*$', pattern) is None:
        return 'invalid pattern', 500
    pattern = pattern.replace(r'*', r'[[A-Za-z0-9_]*')
    dag_ids = [dag_id.decode('utf-8') for dag_id in get_redis_client().smembers(REDIS_KEYS['all_dag_ids'])]
    return json.dumps(list(filter(lambda dag_id: re.match(pattern, dag_id) is not None, dag_ids)))
