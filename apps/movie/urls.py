#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import views as view_api


urlpatterns = [
    url('^movie$', view_api.MovieList.as_view(), name='apps.movie.MovieList'),
    url('^movie/(?P<id>[0-9]{1,128})$', view_api.MovieDetail.as_view(), name='apps.movie.MovieDetailApi'),
    url('^movie/(?P<movie_id>[0-9]{1,128})/links$', view_api.LinkList.as_view(), name='apps.movie.MovieListApi'),
]
html_urlpatterns = [
    # url('^book$', view_html.BookList.as_view(), name='apps.eBook.BookListHtml'),
    # url('^movie/detail/(?P<id>[0-9]{1,128})$', view_html.BookDetail.as_view(), name='apps.movie.BookDetailHtml'),
    # url('^e-book/(?P<book_id>[0-9]{1,128})/links$', view_html.LinkList.as_view(), name='apps.eBook.LinkListHtml'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
html_urlpatterns = format_suffix_patterns(html_urlpatterns)
