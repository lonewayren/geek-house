#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
import time

from lib.robot import BaseFilter
from apps.eBook.serializers import Book
from django.core.cache import cache


def get_access_token(robot_client_instance):
    """
    判断现有的token是否过期。
    用户需要多进程或者多机部署,现在手动重写这个函数
    来自定义token的存储，刷新策略。

    :return: 返回token
    """
    key = "wx_client_access_token"
    if cache.has_key(key):
        print 'get cache token!!!'
        token = cache.get(key)
        ttl = cache.ttl(key)
    else:
        print 'get new token!!!'
        json = robot_client_instance.grant_token()
        token = json["access_token"]
        ttl = json["expires_in"] - 60
        cache.set(key, token, timeout=ttl)
    setattr(robot_client_instance, 'token_expires_at', int(time.time()) + ttl)
    setattr(robot_client_instance, '_token', token)
    return token


class BookTitleFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        self.exist = kwargs.pop('exist', True)
        super(BaseFilter, self).__init__(*args, **kwargs)

    def handler(self, msg):
        if self.exist:
            return Book.objects.filter(title__icontains=msg, links__valid=True).exists()
        else:
            return not Book.objects.filter(title__icontains=msg, links__valid=True).exists()


class KeyWordsFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        self.keywords = kwargs.pop('keywords', {})
        super(BaseFilter, self).__init__(*args, **kwargs)

    def handler(self, msg):
        if self.keywords:
            return msg in self.keywords.keys()
        return False


def unLog(value):
    for key in ['呀', '吗', '?']:
        if key in value:
            return True
    if value in ['下载码', '我的信息查询', '提取码']:
        return True
    return False
