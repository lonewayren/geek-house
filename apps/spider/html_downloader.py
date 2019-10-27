#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
"""
Created on Thu Feb  8 11:43:09 2018

@author: 周立凤
"""
import requests


class HtmlDownloader(object):
    
    def download(self, url, code=68682019):
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"e_secret_key\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % code
        headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                }
        response = requests.request("POST", url, data=payload, headers=headers, timeout=15, verify=True)
        return response
