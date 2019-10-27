#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'

from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google
from django.conf import settings

import requests

from apps.eBook.models import Book
from django.urls import reverse

class BookDetailSiteMap(Sitemap):
    changefreq = "weekly"
    priority = "0.6"

    def items(self):
        return Book.objects.all()

    def location(self, item):
        return reverse('apps.eBook.BookDetailHtml', kwargs={'id': item.id})

print Site.objects.get_current().domain


class SpiderNotify():
    def __init__(self):
        self.domain = Site.objects.get_current().domain

    @staticmethod
    def baidu_notify(urls, _type):
        try:
            data = '\n'.join(urls)
            result = requests.post(_type, data=data)
            print result.status_code, result.text
        except Exception as e:
            print e.message

    @staticmethod
    def bing_notify(urls, _type):
        domain = Site.objects.get_current().domain
        try:
            data = {
                "siteUrl": "https://%s" %(domain,),
                "urlList": urls
            }
            result = requests.post(_type, json=data)
            print result.status_code, result.text
        except Exception as e:
            print e.message

    @staticmethod
    def __google_notify():
        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            print e.message
