#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on Thu Feb  8 11:42:36 2018

@author: 周立凤
"""


class UrlManager(object):
    def __init__(self, start, end):
        self.new_urls = []
        self.start = start
        self.end = end

    @property
    def num(self):
        return self.new_urls.__len__()

    def add_new_url(self): 
        for source_id in range(self.start, self.end):
            self.new_urls.append("https://5kindle.com/books/%s/" % source_id)

    def had_spider(self):
        return self.new_urls.__len__()
    
    def get_new_url(self):
        if self.new_urls:
            return self.new_urls.pop()
        return None