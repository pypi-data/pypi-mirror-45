# -*- coding: utf-8 -*-
# @Time    : 2019-04-15 19:42
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: setup.py
# @Software: PyCharm
from setuptools import find_packages, setup

setup(
    name='dag_manager',
    version='0.1.1a',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',

    ],
)