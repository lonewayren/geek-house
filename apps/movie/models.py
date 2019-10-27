# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.functional import cached_property
from django.db import models

# Create your models here.


class Movie(models.Model):

    id = models.AutoField(verbose_name='电影ID', primary_key=True)
    title = models.CharField(verbose_name='电影名称', max_length=75, blank=False, null=False, default='')
    author = models.CharField(verbose_name='导演', max_length=25, blank=True, null=True, default='')
    star = models.CharField(verbose_name='演员', max_length=75, blank=True, null=True, default='')
    cover = models.CharField(verbose_name='封面', max_length=255, blank=True, null=True, default='')
    cover_bk = models.CharField(verbose_name='封面备份', max_length=255, blank=True, null=True, default='')

    language = models.CharField(verbose_name='语言', max_length=25, blank=True, null=True, default='')
    age = models.CharField(verbose_name='年代', max_length=25, blank=True, null=True, default='')
    area = models.CharField(verbose_name='地区', max_length=25, blank=True, null=True, default='')
    score = models.FloatField(verbose_name='评分', blank=True, null=True, default=0.0)
    online_date = models.DateField(verbose_name='上映时间', blank=True, null=True)
    comments = models.URLField(verbose_name='豆瓣短评', blank=True, null=True)

    category = models.ManyToManyField(verbose_name='分类标签',to='Category', related_name='movies',db_constraint=False,)
    description = models.TextField(verbose_name='简介', blank=True, null=True, default='')
    source = models.ForeignKey(verbose_name='外部来源', to='Source', related_name='movies', db_constraint=False,)
    source_uid = models.IntegerField(verbose_name='外部ID', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "电影"
        index_together = ['title', 'author', 'source_uid']

    @cached_property
    def source_types(self):
        return self.links.values_list('type', flat=True).distinct()

    def __unicode__(self):
        return '%s' % self.title


class Source(models.Model):
    
    id = models.AutoField(verbose_name='来源ID', primary_key=True)
    host = models.CharField(verbose_name='来源网址', max_length=50, blank=True, null=True, default='')

    class Meta:
        verbose_name = verbose_name_plural = "来源"
        index_together = ['host']
        unique_together = ['id', 'host']

    def __unicode__(self):
        return "%s" % self.host


class Category(models.Model):
    id = models.AutoField(verbose_name='标签ID', primary_key=True)
    name = models.CharField(verbose_name='分类名称', max_length=50, blank=True, null=True, default='')

    class Meta:
        verbose_name = verbose_name_plural = "标签分类"
        index_together = ['name']
        unique_together = ['id', 'name']

    def __unicode__(self):
        return "%s" % self.name

    def seralize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Link(models.Model):
    TYPE_CHOICES = (
        ('xl', '迅雷连接'),
        ('cl', '磁力连接'),
        ('zx', '在线连接'),
        ('bd', '百度网盘'),
    )
    DPI_CHOICES = (
        ('sm', '小屏'),
        ('lg', '大屏'),
        ('hd', '平板'),
        ('4k', '原画'),
        ('yb', '云播'),
    )
    id = models.AutoField(verbose_name='链接ID', primary_key=True)
    movie = models.ForeignKey(verbose_name=u"图书", to='Movie', related_name='links', db_constraint=False,)
    link = models.CharField(verbose_name='链接', max_length=512, blank=False, null=False, default='')
    type = models.CharField(verbose_name='链接类型', max_length=25, choices=TYPE_CHOICES, blank=False, null=False, default='')
    definition = models.CharField(verbose_name='清晰度', max_length=25, choices=DPI_CHOICES, blank=False, null=False, default='')
    secret = models.CharField(verbose_name='密码', max_length=25, blank=True, null=True, default='')
    valid = models.BooleanField(verbose_name='是否有效', blank=False, null=False, default=True)

    class Meta:
        verbose_name = verbose_name_plural = "链接"
        index_together = ['link']


class Search(models.Model):
    id = models.AutoField(verbose_name='查找ID', primary_key=True)
    value = models.CharField(verbose_name='查找内容', max_length=255, blank=True, null=True, default='')
    user = models.ForeignKey(verbose_name=u"所属用户", to='account.WxUser', related_name='movie_searches', db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = "搜索记录"

    def __unicode__(self):
        return u'%s' % self.value
