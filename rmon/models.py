#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 15:01
# @Author  : Hython.com
# @File    : models.py
"""rmon.models
该模块实现了所有的model类及相应的序列化类
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Server(db.Model):
    """Redis 服务器模型"""
    __tablename__ = 'redis_server'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True) # unique=true 不能有重名服务器
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):
        """保存到数据库中"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """从数据库中删除"""
        db.session.delete(self)
        db.session.commit()