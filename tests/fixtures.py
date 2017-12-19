#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 22:09
# @Author  : Hython.com
# @File    : fixtures.py
import pytest

from rmon.app import create_app
from rmon.models import Server
from rmon.models import db as database


@pytest.fixture
def app():
    """Flask app"""
    return create_app()


@pytest.yield_fixture
def db(app):
    """数据库"""
    with app.app_context():
        database.create_all()
        yield db
        database.drop_all()


@pytest.fixture
def server(db):
    """测试Redis服务器记录"""
    server = Server(name='redis_test', description='this is a test record',
                    host='127.0.0.1', port='6379')
    server.save()
    return server