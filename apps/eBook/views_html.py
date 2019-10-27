# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import traceback
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.generic import TemplateView


from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from django.shortcuts import Vi
from rest_framework import status
from django.http.response import HttpResponse
from django.core.cache import cache
from django.db import transaction
from django.conf import settings

from lib.utils import bookVerifyCodeUtils
from lib.restful import ClientParamsInvalidError, SUCCESS, FAILURE
from apps.eBook.serializers import Book, Link, BookListSerializer, BookDetailSerializer, LinkSerializer
from apps.account.serializers import WxUser, WxUserSerializer
from apps.account.utils import init_wx_user
# Create your views here.


class BookList(ListView):
    template_name = 'html/index.html'

    model = Book
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    page_type = ''
    ordering = ('id',)

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page


class BookDetail(DetailView):
    
    template_name = 'html/detail.html'
    model = Book
    pk_url_kwarg = 'id'
    context_object_name = "book"

