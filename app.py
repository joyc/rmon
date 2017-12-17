#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 14:34
# @Author  : Hython.com
# @File    : app.py.py
"""
app.py
应用入口文件
"""
import urllib
from rmon.app import create_app
from rmon.models import db


app = create_app()

@app.cli.command()
def routes():
    """输出app中定义的所有路由"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:25s} {:35s} {:20s}".format(
            rule.endpoint, methods, str(rule)))
        output.append(line)

    for line in sorted(output):
        print(line)

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    print("sqlite3 database file is %s" % app.config['SQLALCHEMY_DATABASE_URI'])
