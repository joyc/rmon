#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 14:50
# @Author  : Hython.com
# @File    : config.py
"""
rmon.config
rmon的配置文件
"""
import os


class DevConfig:
    """开发环境配置信息"""

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True


class ProductConfig:
    """生产环境配置信息"""

    DEBUG = False

    # sqlite 数据库文件路径
    path = os.path.join(os.getcwd(), 'rmon.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path