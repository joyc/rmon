#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/22/0022 0:35
# @Author  : Hython.com
# @File    : test_views.py
import json
from flask import url_for

from rmon.models import Server


class TestServerList:
    """测试 Redis 服务器列表 API
    """

    endpoint = 'api.server_list'

    def test_get_servers(self, server, client):
        """获取 Redis 服务器列表
        """
        resp = client.get(url_for(self.endpoint))

        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        # 访问成功后返回状态码 200 OK
        assert resp.status_code == 200

        servers = resp.json

        # 由于当前测试环境中只有一个 Redis 服务器，所以返回的数量为 1
        assert len(servers) == 1

        h = servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self, db, client):
        """测试创建 Redis 服务器成功
        """
        # 自行补充
        pass

    def test_create_server_failed_with_invalid_host(self, db, client):
        """无效的服务器地址导致创建 Redis 服务器失败
        """
        # 自行补充
        pass

    def test_create_server_failed_with_duplciate_server(self, server, client):
        """创建重复的服务器时将失败
        """
        # 自行补充
        pass