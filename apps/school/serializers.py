#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from .models import Work, Company


class CompanySerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class WorkSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Work
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()
