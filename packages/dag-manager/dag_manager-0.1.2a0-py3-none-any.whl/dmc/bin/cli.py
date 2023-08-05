# -*- coding: utf-8 -*-
# @Time    : 2019-04-15 14:49
# @Author  : WuTong
# @Email   : twu@aibee.com
# @FileName: cli.py
# @Software: PyCharm
import argparse
import json
import os
from collections import namedtuple

from dmc.dmc import DagManagerClient

Arg = namedtuple(
    'Arg', ['flags', 'help', 'action', 'default', 'nargs', 'type', 'choices', 'required', 'metavar'])
Arg.__new__.__defaults__ = (None, None, None, None, None, None, None)

with open(os.path.join(os.getenv('HOME'), '.mdc/config')) as f:
    conf = json.load(f)
base_url = conf['base_url']
storage_path = conf.get('storage_path') or os.getenv('MDC_DAG_HOME', os.getcwd())
dmc = DagManagerClient(base_url, storage_path)


def get(parsed_args):
    dmc.get(parsed_args.dag_id)


def getall(parsed_args):
    dmc.get()


def upload(parsed_args):
    dmc.upload(parsed_args.dag_id, parsed_args.file, parsed_args.dag_path)


def remove(parsed_args):
    dmc.remove(parsed_args.dag_id)


def ls(parsed_args):
    dag_ids = dmc.list(parsed_args.pattern)
    for dag_id in dag_ids:
        print(dag_id)


class CLIFactory(object):
    args = {
        'dag_id': Arg(('dag_id',), 'dag_id'),
        'file': Arg(('-f', '--file'), 'file to be uploaded'),
        'pattern': Arg(('-p', '--pattern'), 'pattern to be matched'),
        'dag_path': Arg(('-dp', '--dag_path'), 'path to the dag file, must specified when upload a zip file'),
    }
    subparsers = (
        {
            'func': ls,
            'help': 'list dags in DagManager by matching pattern',
            'args': ('pattern',)
        }, {
            'func': get,
            'help': 'get a dag from DagManager by dag_id',
            'args': ('dag_id', ),
        }, {
            'func': getall,
            'help': 'get all dags from DagManager',
            'args': tuple(),
        }, {
            'func': remove,
            'help': 'remove a dag from DagManager by dag_id',
            'args': ('dag_id', ),
        }, {
            'func': upload,
            'help': 'upload a dag to DagManager by dag_id',
            'args': ('dag_id', 'file', 'dag_path'),
        }
    )
    subparsers_dict = {sp['func'].__name__: sp for sp in subparsers}

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(
            help='sub-command help', dest='subcommand')
        subparsers.required = True
        subparser_list = cls.subparsers_dict.keys()
        for sub in subparser_list:
            sub = cls.subparsers_dict[sub]
            sp = subparsers.add_parser(sub['func'].__name__, help=sub['help'])
            for arg in sub['args']:
                arg = cls.args[arg]
                kwargs = {
                    f: getattr(arg, f)
                    for f in arg._fields if f != 'flags' and getattr(arg, f)}
                sp.add_argument(*arg.flags, **kwargs)
            sp.set_defaults(func=sub['func'])
        return parser

