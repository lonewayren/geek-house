#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import views as view_api
import views_html as view_html


urlpatterns = [
    url('^e-book$', view_api.BookList.as_view(), name='apps.eBook.BookListApi'),
    url('^e-book/(?P<id>[0-9]{1,128})$', view_api.BookDetail.as_view(), name='apps.eBook.BookDetailApi'),
    url('^e-book/(?P<book_id>[0-9]{1,128})/links$', view_api.LinkList.as_view(), name='apps.eBook.LinkListApi'),
]
html_urlpatterns = [
    # url('^book$', view_html.BookList.as_view(), name='apps.eBook.BookListHtml'),
    url('^book/detail/(?P<id>[0-9]{1,128})$', view_html.BookDetail.as_view(), name='apps.eBook.BookDetailHtml'),
    # url('^e-book/(?P<book_id>[0-9]{1,128})/links$', view_html.LinkList.as_view(), name='apps.eBook.LinkListHtml'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
html_urlpatterns = format_suffix_patterns(html_urlpatterns)
