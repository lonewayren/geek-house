#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
from serializers import WxUserSerializer
INIT_TOTAL = 5


def init_wx_user(openID, name, **kwargs):
    data = {
        'id': openID,
        'name': name,
        'active': True,
        'total': INIT_TOTAL,
        'used': 0
    }
    data.update(kwargs)
    return WxUserSerializer(data=data).shortcut_create(raise_exception=True)
