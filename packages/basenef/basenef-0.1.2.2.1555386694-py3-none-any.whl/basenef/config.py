# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: config.py
@date: 4/15/2019
@desc:
'''
import os
from .utils import separator

''' required directories'''
DATABASE_DIR = os.environ['HOME'] + separator + 'Database_nef' + separator
RESOURCE_DIR = DATABASE_DIR + 'resources' + separator
SCHEMA_DIR = DATABASE_DIR + 'schemas' + separator
CACHE_DIR = DATABASE_DIR + 'caches' + separator
LOG_DIR = DATABASE_DIR + 'logs' + separator
DOC_DIR = DATABASE_DIR + 'docs' + separator

_PATH_LIST = [DATABASE_DIR, RESOURCE_DIR, SCHEMA_DIR, CACHE_DIR, LOG_DIR, DOC_DIR]

for _path in _PATH_LIST:
    if not os.path.isdir(_path):
        os.mkdir(_path)
