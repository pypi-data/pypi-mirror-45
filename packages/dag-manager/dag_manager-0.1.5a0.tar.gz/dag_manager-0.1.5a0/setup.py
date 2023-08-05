# -*- coding: utf-8 -*-
# @Time    : 2019-04-15 19:42
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: setup.py
# @Software: PyCharm
from setuptools import find_packages, setup

setup(
    name='dag_manager',
    version='0.1.5a',
    author='wutong',
    author_email='twu@aibee.com',
    description='Manage airflow dags, synchronize updates to scheduler and webserver, '
    'so airflow does not depend on shared file system',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    url='http://gitlab.aibee.cn/platform/dag-manager',
    install_requires=[
        'flask==1.0.2',
        'requests==2.21.0',
        'redis==3.2.1',
        'apache-airflow==1.10.3',
    ],
    scripts=['dmc/bin/dmc']
)
