#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *


urlpatterns = (
    url('^school/work$', WorkList.as_view(), name='apps.school.WorkList'),

)


urlpatterns = format_suffix_patterns(urlpatterns)
