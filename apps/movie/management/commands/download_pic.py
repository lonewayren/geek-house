#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
import os
from openpyxl import load_workbook
from django.core.management.base import BaseCommand, CommandError
from apps.eBook.serializers import Book, Link, Source, Category, BookListSerializer, LinkSerializer, CategorySerializer
from django.db import transaction
from django.conf import settings
from urlparse import urljoin
import requests
from hashlib import md5

ERROR_LIST = []


def download():
    books = Book.objects.filter().exclude(cover__in=['']).all()
    bookCoverDir = os.path.join(settings.BASE_DIR, 'static/bookCovers/5kindle')
    for book in books[::]:
        try:
            if book.cover and not book.cover_bk:
                pic_type = book.cover.split('.')[-1]
                md5Str = md5()
                str2sign = '/'.join([book.source.host, book.source_uid.__str__()])
                md5Str.update(str2sign)
                filename = "%s.%s" % (md5Str.hexdigest(), pic_type)
                filepath = "%s/%s" % (bookCoverDir, filename)
                resp = requests.get(book.cover.replace('https://', 'https://images.weserv.nl/?url='), verify=False)
                if resp.status_code == 200:
                    with open(filepath, 'wr') as f:
                        f.write(resp.content)
                    book.cover_bk = filename
                    book.save()
        except Exception as e:
            print e.message


class Command(BaseCommand):
    def handle(self, *args, **options):
        download()
