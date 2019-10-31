#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.cache import cache
from urlparse import urljoin

from geekHouse.sitemap import SpiderNotify
from apps.eBook.serializers import Book
from django.conf import settings

BOOK_ID_LIST = 'books'
cache_client = cache.client.get_client()
NOTIFY = {
    'pc': {
        'NOTIFY_NUM': 24,
        'QUEUE_NAME': 'books_pc',
        '_type': settings.BAIDU_NOTIFY_URL_PC
    },
    'week': {
        'NOTIFY_NUM': 24,
        'QUEUE_NAME': 'books_week',
        '_type': settings.BAIDU_NOTIFY_URL_MB_WEEK
    },
    'day': {
        'NOTIFY_NUM': 10,
        'QUEUE_NAME': 'books_day',
        '_type': settings.BAIDU_NOTIFY_URL_MB_DAY
    },
    'bing': {
        'NOTIFY_NUM': 10,
        'QUEUE_NAME': 'books_bing',
        '_type': settings.BING_NOTIFY_URL_MB_DAY
    },
}


def init_queue(_type):
    _type = NOTIFY[_type]['QUEUE_NAME']
    books = Book.objects.filter(links__valid=True).all()
    for book in books:
        cache_client.rpush(_type, book.id)


def notify(options):
    _type = options['type']
    if options['init']:
        init_queue(_type)
    book_id_list = []
    conf = NOTIFY[_type]
    notify_num, base_url, queue_name = conf['NOTIFY_NUM'], conf['_type'], conf['QUEUE_NAME']
    if not cache_client.exists(queue_name):
        init_queue(_type)
    for i in range(notify_num):
        book_id = cache_client.lpop(queue_name)
        if book_id:
            book_id_list.append(book_id)
    if not book_id_list:
        return
    domain = "https://%s" % settings.DOMAIN
    urls = [urljoin(domain, reverse('apps.eBook.BookDetailHtml', kwargs={'id': book_id})) for book_id in book_id_list]
    print urls
    if _type in ('pc', 'week', 'day'):
        SpiderNotify.baidu_notify(urls, base_url)
    elif _type in ('bing',):
        SpiderNotify.bing_notify(urls, base_url)
    else:
        pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--init',
            action='store',
            dest='init',
            required=False,
            default='',
            help='init notify',
        )
        parser.add_argument(
            '-t',
            '--type',
            action='store',
            dest='type',
            required=False,
            default='pc',
            help='init notify',
        )

    def handle(self, *args, **options):
        notify(options)
