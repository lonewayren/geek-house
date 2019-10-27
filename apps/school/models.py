# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.AutoField(verbose_name='公司ID', primary_key=True)
    name = models.CharField(verbose_name='公司名称', max_length=75, null=True, blank=True)
    logo = models.CharField(verbose_name='公司logo', max_length=25, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "公司"
        index_together = ['id', 'name', 'logo']

    def __unicode__(self):
        return "%s" % self.name


class Work(models.Model):
    id = models.AutoField(verbose_name='工作ID', primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=255, null=True, blank=True)
    href = models.URLField(verbose_name='连接')
    hot = models.BooleanField(verbose_name='进行中')
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    company = models.ForeignKey(verbose_name='所属公司', to='Company', related_name='school_works', db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = "招聘"
        index_together = ['id', 'title', 'href', 'hot']

    def __unicode__(self):
        return "%s" % self.title



