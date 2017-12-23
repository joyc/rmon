#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/19/0017 23:52
# @Author  : Hython.com
# @File    : server.py
"""rmon.views.server
实现了所有的视图控制器
"""
from flask import request, g

from rmon.common.rest import RestView
from rmon.models import Server, ServerSchema


class ServerList(RestView):
    """Redis 服务器列表
    """

    def get(self):
        """获取Redis列表"""
        servers = Server.query.all()
        return ServerSchema().dump(servers, many=True).data

    def post(self):
        """创建Redis服务器"""
        data = request.get_json()
        server, errors = ServerSchema().load(data)
        if errors:
            return errors, 400
        server.ping()
        server.save()
        return {'ok': True}, 201
