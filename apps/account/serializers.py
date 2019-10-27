#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from .models import WxUser


class WxUserSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = WxUser
        read_only_fields = ('remain',)
        fields = ('remain', 'id', 'name', 'created_time', 'last_mod_time', 'active', 'used', 'total')

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()