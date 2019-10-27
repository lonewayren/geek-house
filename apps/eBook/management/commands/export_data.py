#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
import os
from openpyxl import load_workbook
from django.core.management.base import BaseCommand, CommandError
from apps.eBook.serializers import Book, Link, Source, Category, BookListSerializer, LinkSerializer, CategorySerializer
from django.db.models import Q
from django.db import transaction
from django.conf import settings
import codecs

ERROR_LIST = []


def export_data():
    # filename = os.path.join(settings.BASE_DIR, 'apps/spider/link_no_code.txt')
    # with open(filename) as f:
    #     loop = True
    #     while loop:
    #         line = loop = f.readline()
    #         print repr(line)
    filename = os.path.join(settings.BASE_DIR, 'apps/spider/link_with_code.txt')
    with codecs.open(filename, 'w+', 'utf-8') as f:
        secret_links = Link.objects.filter(~Q(secret='')).all()
        for link in secret_links:
            content = "%s----%s\r\n" % (link.link, link.secret)
            print content
            f.write(content)
    filename = os.path.join(settings.BASE_DIR, 'apps/spider/link_no_code.txt')
    with codecs.open(filename, 'w+', 'utf-8') as f:
        secret_links = Link.objects.filter(Q(secret='')).all()
        for link in secret_links:
            content = "%s\r\n" % (link.link,)
            print content
            f.write(content)


class Command(BaseCommand):
    def handle(self, *args, **options):
        export_data()
