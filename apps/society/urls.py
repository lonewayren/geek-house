#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.society.views import *


urlpatterns = (
    url('^society/work$', WorkList.as_view(), name='apps.society.WorkList'),

)


urlpatterns = format_suffix_patterns(urlpatterns)
