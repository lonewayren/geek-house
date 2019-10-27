# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now

# Create your models here.


class WxUser(models.Model):

    id = models.CharField(verbose_name='openID', max_length=30, primary_key=True)
    name = models.CharField(verbose_name='昵称', max_length=50, blank=True, null=True, default='')
    created_time = models.DateTimeField('关注时间', blank=False, null=False, default=now)
    last_mod_time = models.DateTimeField('最近登录', blank=False, null=False, auto_now=True)
    active = models.BooleanField(verbose_name='活动', blank=False, null=False, default=True)
    total = models.IntegerField(verbose_name='总下载次数', blank=False, null=False, default=5)
    used = models.IntegerField(verbose_name='已下载次数', blank=False, null=False, default=0)

    class Meta:
        verbose_name = verbose_name_plural = "微信用户"
        unique_together = ['id']
        index_together = ['id', 'name', 'active', 'total', 'used']

    @property
    def remain(self):
        return self.total - self.used
    
    def __unicode__(self):
        return '%s' % self.id

