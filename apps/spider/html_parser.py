#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
"""
Created on Thu Feb  8 11:43:44 2018

@author: 周立凤
"""
from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    
    def _get_new_data(self, soup):
        title = ''
        category = ''
        description = ''
        secret = ''
        link = ''
        cover = 0

        # 解析书名
        try:
            elem_title = soup.find('header', class_='article-header').find('h1')
        except AttributeError:
            elem_title = None
        if elem_title and elem_title.get_text():
            title = elem_title.get_text()

        # 解析分类
        elem_category = soup.find('span', id='mute-category')
        if elem_category and elem_category.get_text():
            category = elem_category.get_text().strip()
        # print category
        # if category in ['好书推荐', '书目推荐']:
        #     return q,title,category,description,d,e,cover

        # 解析简介
        elem_description = soup.find('article', class_='article-content')
        if elem_description:
            flag = False
            for item in elem_description:
                if flag and item.get_text():
                    description = item.get_text()
                    break
                if item.name in ['h2', 'h3', 'h4'] and '内容' in item.get_text():
                    flag = True

        # 解析网盘密码
        if soup.find('p', string=re.compile(r'网盘密码：百度网盘密码：')):
            elem_secret = soup.find('p', string=re.compile(r'网盘密码：百度网盘密码：'))
            reg = r'网盘密码：百度网盘密码：(.{4})'
            wordreg = re.compile(reg)
            secret = "".join(re.findall(wordreg, elem_secret.get_text()))
        elif soup.find_all('div', class_='e-secret'):
            elem_secret = soup.find_all('div', class_='e-secret')
            flag1 = False
            if len(elem_secret) and elem_secret:
                for j in elem_secret:
                    for jj in j:
                        if jj.name == 'strong':
                            secret = jj.get_text()
                            flag1 = True
                            break
                if flag1 is False:
                    secret = j.get_text()
        elif category in ['好书推荐', '书目推荐']:
            pass
        else:
            print '解析网盘密码失败'

        # 解析网盘链接
        elem_link = soup.find('a', href=re.compile(r"//pan.baidu.com/"))
        if elem_link and elem_link['href']:
            link = elem_link['href'].replace('https://5kindle.com/go/?url=', '')
        # print '百度链接:%s' % link

        # 解析图书封面图片
        try:
            elem_cover = soup.find('article', class_='article-content').find('p').find('img', src=re.compile(r"https://5kindle.com/(.*)jpg"))
        except AttributeError:
            elem_cover = None
        if elem_cover and elem_cover['src']:
            cover = elem_cover['src']
        # print '图书封面:%s' % cover

        return title, category, description, secret, link, cover
    
    def pase(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return None
        soup = BeautifulSoup(html_cont, 'html.parser')
        source_id = "".join(re.findall(".*books/(.*)/.*",page_url))
        title, category, description, secret, link, cover = self._get_new_data(soup)
        book = Book(**{
            'source_url': page_url,
            'source_id': source_id,
            'title': title,
            'category': category,
            'description': description,
            'secret': secret,
            'link': link,
            'cover': cover
        })
        return book


class Book(object):

    def __init__(self, **kwargs):
        self.attr_list = ('source_id', 'title', 'category', 'description', 'secret', 'link', 'cover')
        self.source_url = kwargs.get('source_url', '')
        for attr in self.attr_list:
            setattr(self, attr, kwargs.get(attr, ''))

    @property
    def success(self):
        return bool(self.title and self.link)

    def __unicode__(self):
        return "%s %s" % (self.link, self.success)

    def __str__(self):
        return "%s %s" % (self.link, self.success)