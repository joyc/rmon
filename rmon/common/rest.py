#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/12/20/0020 0:11
# @Author  : Hython.com
# @File    : rmon.common.rest.py


class RestException(Exception):
    """异常基类"""
    def __init__(self, code, message):
        """初始化异常
        Aargs:
            code(int): http状态码
            message(str): 错误信息
        """
        self.code = code
        self.message = message
        super(RestException, self).__init__()
