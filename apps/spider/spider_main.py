#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import traceback

"""
Created on Thu Feb  8 11:40:21 2018

@author: 周立凤
"""

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self, start, end):
        self.urls = url_manager.UrlManager(start, end + 1)
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.code_list = ('68682019', '68682018')
        
    def craw(self):
        count = 0
        failed_list = []
        self.urls.add_new_url()
        # 添加所有待爬数据
      
        while self.urls.num > 0:
            try:   
                # 取出一个待爬网页
                new_url = self.urls.get_new_url()
                if not new_url:
                    continue
                print '已爬取%s,剩余%s,正爬取 %s' % (count, self.urls.num, new_url),
                book = code = None
                for code in self.code_list:
                    resp = self.downloader.download(new_url, code=code)
                    # print '已爬取%s,剩余%s,正爬取 %s, code%s' % (count, self.urls.num, new_url, resp.status_code),
                    if resp.status_code == 404:
                        self.outputer.add_not_found(new_url)
                        break
                    book = self.parser.pase(new_url, resp.content)
                    if resp.status_code == 200 and book.success:
                        break
                print resp.status_code, book, code
                if book:
                    self.outputer.collect_data(book)
            except Exception as e:
                failed_list.append(new_url)
                print traceback.format_exc()
            finally:
                count += 1
           
        self.outputer.output()
        self.outputer.statis()

            
if __name__ == "__main__":
    step = 1000
    for index in range(71000, 10000, -step):
        start, end = index-step, index
        obj_spider = SpiderMain(start, end)
        obj_spider.craw()
