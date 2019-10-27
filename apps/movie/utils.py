#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals, absolute_import

from django.db import transaction
from apps.account.models import WxUser
from apps.eBook.models import Search


class SearchManager(object):
    def __init__(self):
        pass

    @transaction.atomic()
    def log_unhit_search(self, value, user):
        assert isinstance(user, WxUser), TypeError('user must be WxUser instance')
        if not Search.objects.filter(value=value, user=user).exists():
            Search(**{'value': value, 'user': user}).save()
            return True
        else:
            return False

    def count_search(self, **kwargs):
        return Search.objects.filter(**kwargs).count()


search_manager = SearchManager()
