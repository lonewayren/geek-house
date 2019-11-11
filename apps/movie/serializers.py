#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from .models import Movie, Link, Source, Category
from lib.restful import ModifyJSONField


class CategorySerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class MovieListSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Movie
        read_only_fields = ('links',)
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class MovieDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    source_types = serializers.ListField(read_only=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Movie
        read_only_fields = ('source_types', )
        fields = ('source_types', 'id', 'title', 'author', 'cover', 'description', 'language', 'star', 'age', 'area', 'score', 'online_date', 'comments', 'category')

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class LinkSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class SourceSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Source
        fields = '__all__'

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()


class MovieLinkSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    links = LinkSerializer(many=True)

    class Meta:
        model = Movie
        read_only_fields = ('links',)
        fields = ('links', 'id', 'title', 'author', 'cover', 'description')

    def shortcut_create(self, raise_exception=True):
        self.is_valid(raise_exception=raise_exception)
        return self.save()
