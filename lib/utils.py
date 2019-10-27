#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
from django.core.cache import cache
from random import randint

import traceback


class VerifyCode(object):

    def __init__(self):
        self.KEY_PREFIX = 'varify_code_%s'
        pass

    def key_func(self, code):
        return self.KEY_PREFIX % code

    def gen_verify_code(self, value='', ttl=120):
        while True:
            code = randint(100000, 999999).__str__()
            key = self.key_func(code)
            if cache.set(key, value, timeout=ttl, nx=True):
                return code

    def confirm_verify_code(self, code):
        access, msg = False, ''
        try:
            if code is None:
                msg = "验证码不能为空"
            if not code.isdigit() or code.__len__() != 6:
                msg = "验证码格式错误"
            key = self.key_func(code)
            content = cache.get(key)
            # todo: delete on prod
            # if code == '999999':
            #     access, msg = True, 'ohfeQ0p4wrKLiz0aPMDKAuCHsgAE'
            #     return
            if not content:
                msg = '验证码无效'
            else:
                cache.delete(key)
                access, msg = True, content
        except Exception as e:
            msg = "验证码校验失败"
            traceback.print_exc()
        finally:
            return access, msg


bookVerifyCodeUtils = VerifyCode()
movieVerifyCodeUtils = VerifyCode()

