#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 16:00
# @Author  : Hython.com
# @File    : app.py
"""rmon.app
该模块主要实现了app创建函数
"""
import os
from flask import Flask

from rmon.views import api
from rmon.models import db
from rmon.config import DevConfig, ProductConfig


def create_app():
    """创建并初始化 Flask app"""

    app = Flask('rmon')

    # 根据环境变量加载开发环境或者生产环境配置
    env = os.environ.get('RMON_ENV')

    if env in ('pro', 'prod', 'product'):
        app.config.from_object(ProductConfig)
    else:
        app.config.from_object(DevConfig)

    # 从环境变量RMON_SETTINGS指定的文件中加载配置
    app.config.from_envvar('RMON_SETTINGS', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 注册Blueprint
    app.register_blueprint(api)
    # 如果是开发环境则创建所有数据库表
    if app.debug:
        with app.app_context():
            db.create_all()
    return app