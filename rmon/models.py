#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/17/0017 15:01
# @Author  : Hython.com
# @File    : models.py
"""rmon.models
该模块实现了所有的model类及相应的序列化类
"""
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis, RedisError
from datetime import datetime
from rmon.common.rest import RestException
from marshmallow import (Schema, fields, validate, post_load,
                        validates_schema, ValidationError)


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

    @property
    def redis(self):
        return StrictRedis(host=self.host, port=self.port,
                           password=self.password)

    def ping(self):
        """检查 Redis 服务器是否可以访问"""
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)

    def get_metrics(self):
        """获取 Redis 服务器监控信息
        通过 Redis 服务器指令 INFO 返回监控信息, 参考 https://redis.io/commands/INFO
        """
        try:
            # TODO 新版本的 Redis 服务器支持查看某一 setion 的信息，不必返回所有信息
            return self.redis.info()
        except RedisError:
            raise RestException(400, 'redis server %s can not connected' % self.host)


class ServerSchema(Schema):
    """Redis服务器记录序列化"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(2, 64))
    description = fields.String(validate=validate.Length(0, 512))
    # 正则检验Ip v4 地址格式
    host = fields.String(validate=validate.Regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    port = fields.Integer(validate=validate.Range(1024, 65536))
    password = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_schema(self, data):
        """验证是否存在同名redis服务器"""
        if 'port' not in data:
            data['port'] = 6379

        instance = self.context.get('instance', None)

        server = Server.query.filter_by(name=data['name']).first()

        if server is None:
            return

        # 更新服务器时
        if instance is not None and server != instance:
            raise ValidationError('Redis server already exist', 'name')

        # 创建服务器时
        if instance is None and server:
            raise ValidationError('Redis server already exist', 'name')

    @post_load
    def create_or_update(self, data):
        """数据加载成功后自动创建Server对象"""
        instance = self.context.get('instance', None)

        # 创建Redis服务器
        if instance is None:
            return Server(**data)

        # 更新服务器
        for key in data:
            setattr(instance, key, data[key])
        return instance

