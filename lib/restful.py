#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals

import six
import json

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.conf import settings

SUCCESS = 0


class FAILURE:
    clientError = 40000
    bookCodeError = 40001
    bookNotFind = 40401
    serverError = 50000


class ModifyJSONField(serializers.JSONField):

    def to_internal_value(self, data):
        try:
            if self.binary or getattr(data, 'is_json_string', False):
                if isinstance(data, six.binary_type):
                    data = data.decode('utf-8')
                return json.loads(data)
            else:
                data = json.dumps(data)
        except (TypeError, ValueError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        if self.binary:
            value = json.dumps(value)
            # On python 2.x the return type for json.dumps() is underspecified.
            # On python 3.x json.dumps() returns unicode strings.
            if isinstance(value, six.text_type):
                value = bytes(value.encode('utf-8'))
        else:
            value = json.loads(value)
        return value


class MyPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'size'
    max_page_size = 50
    last_page_strings = ('last',)


class ClientParamsInvalidError(Exception):
    def __init__(self, msg='', code=1):
        self.msg = msg
        self.code = code
        Exception.__init__(self, self.msg)


def seo_processor(requests):
    key = 'seo_processor'
    value = cache.get(key)
    if value:
        return value
    else:
        value = {
            'SITE_NAME': settings.SITENAME,
            'SITE_SEO_DESCRIPTION': settings.SITE_SEO_DESCRIPTION,
            'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
            'SITE_KEYWORDS': settings.SITE_KEYWORDS,
            'SITE_BASE_URL': requests.scheme + '://' + requests.get_host() + '/',
        }
        cache.set(key, value, 60 * 60 * 10)
        return value