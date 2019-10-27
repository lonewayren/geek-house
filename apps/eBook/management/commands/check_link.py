#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals, division
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.eBook.models import Link
from bs4 import BeautifulSoup
from django.template import Context, loader
from django.core.mail import send_mail
import re
import time
import json
from datetime import datetime
import urllib2
import cookielib
import urlparse
import logging
import traceback
import requests
import random
import commands

logger = logging.getLogger('manage')


BaiduPCS = settings.PCS


def gethtml(url):
    try:

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        headers = {
            'Referer': 'https://pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) > AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 > MicroMessenger/6.0.1 NetType/WIFI'
        }
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req, None, 15)
        html = response.read()
        code = response.getcode()
        soup = BeautifulSoup(html, 'html.parser')
        return code, soup
    except Exception,e:
        return 1, e


def getValid(codes):
    url = "https://ypsuperkey.meek.com.cn/api/v1/item/check-data"
    payload = "uuids={uuids}&client_version=2019.2".format(uuids=','.join(['BDY-'+code for code in codes]))
    headers = {
        'origin': "chrome-extension://anlllmnpjodopgbkbpnghnjlelnogfjc",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "*/*",
        'accept-encoding': "gzip",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': "popupad=1",
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers, verify=True)
        return response.json()
    except Exception as e:
        logger.error(e.message)
        return {}.fromkeys(['BDY-'+code for code in codes], None)


def old_isValid(soup):
    assert isinstance(soup, BeautifulSoup), TypeError
    if soup.find_all(string=re.compile(r'此链接分享内容可能因为涉')):
        return False
    elif soup.find_all('title', string=re.compile(r'页面不存在')):
        return False
    elif soup.find_all('img', alt=re.compile(r'验证码获取中')):
        return False
    elif soup.find_all('section', string=re.compile(r'分享文件已经被取消')):
        return False
    elif soup.find_all('span', string=re.compile(r'保存到百度网盘')):
        return True
    else:
        return False


def isValid(data_map):
    pass


def old_check():
    links = Link.objects.filter(type='bd').all()[:50:]
    invalid_link_list = []
    for link in links:
        log_msg_list = []
        try:
            if 'surl=' in link.link:
                qs = urlparse.parse_qs(urlparse.urlparse(link.link).query)
                surl = qs.get('surl', ['xxx'])[0]
                link.link = 'https://pan.baidu.com/s/1%s' % surl
            valid = True
            log_msg_list.append(link.id.__str__())
            if link.link:
                if link.secret:
                    url = link.link + '?from=qrcode&passwd=%s' % link.secret
                else:
                    url = link.link
                log_msg_list.append(url)
                status_code, soup = gethtml(url)
                if status_code != 200:
                    log_msg_list.append(status_code.__str__())
                    valid = False
                else:
                    valid = isValid(soup)
                    log_msg_list.append(status_code.__str__())
                    log_msg_list.append(valid.__str__())
            else:
                valid = False
            logger.info(' '.join(log_msg_list))

            link.valid = valid
            if not valid:
                invalid_link_list.append(link)
            link.save()
            time.sleep(3)
        except Exception as e:
            logger.error(e.message)
            traceback.print_exc()
    return links, invalid_link_list


def varify(_link):
    code = _link.link.split('/s/1')[-1]
    if _link.secret:
        cmd = "{BaiduPCS} share p '{code}' --pwd '{pwd}'".format(BaiduPCS=BaiduPCS, code=code, pwd=_link.secret)
    else:
        cmd = "{BaiduPCS} share p '{code}'".format(BaiduPCS=BaiduPCS, code=code)
    s, o = commands.getstatusoutput(cmd)
    if s == 0:
        if "失败".encode('utf-8') in o:
            return False, o
        if json.loads(o).get('fsIds'):
            return True, o
        return False, o
    else:
        return False, o


def check():
    links = Link.objects.filter(type='bd').all()[::]
    interval = 50
    instance_map = {}
    log_msg_map = {}
    invalid_link_list = []
    for link in links:
        log_msg_map[link.id] = [link.id.__str__()]
        try:
            # if 'surl=' in link.link:
            #     qs = urlparse.parse_qs(urlparse.urlparse(link.link).query)
            #     surl = qs.get('surl', ['xxx'])[0]
            #     raw_link = 'https://pan.baidu.com/s/1%s' % surl
            # else:
            #     raw_link = link.link
            # raw_link = raw_link.strip().strip(r'%20')
            # if '#' in raw_link:
            #     raw_link = raw_link.strip('#')[0]
            # if '/s/1' not in raw_link:
            #     log_msg_map[link.id].append('link orror: %s' % raw_link)
            #     continue
            if '/s/1' not in link.link:
                log_msg_map[link.id].append('link format error: %s' % (link.link,))
                continue
            code = link.link.split('/s/1')[-1]
            if not code:
                log_msg_map[link.id].append('parse code error')
                continue
            url = link.link
            log_msg_map[link.id].append(url)
            instance_map[code] = link
            if instance_map.__len__() == interval:
                valid_result_map = getValid(instance_map.keys())
                for raw_code, values in valid_result_map.iteritems():
                    code = raw_code.replace('BDY-', '')
                    try:
                        _link = instance_map[code]
                    except KeyError:
                        logger.error('code error:%s' % raw_code)
                        continue
                    if not values:
                        valid, res = varify(_link)
                        if valid:
                            _link.valid = True
                        else:
                            _link.valid = False
                            invalid_link_list.append(_link)
                        values = res
                    elif values and values.get('state') == 'INVALID':
                        _link.valid = False
                        invalid_link_list.append(_link)
                    elif values and values.get('state') == 'VALID':
                        _link.valid = True
                        if values.get('access_code'):
                            _link.secret = values.get('access_code')
                    else:
                        pass
                    _link.save()
                    log_msg_map[_link.id].append(str(_link.valid))
                    log_msg_map[_link.id].append(str(values))
                for key in sorted(log_msg_map.keys()):
                    logger.info(' '.join(log_msg_map[key]))
                instance_map = {}
                log_msg_map = {}
                time.sleep(random.randrange(0, 10))
        except Exception as e:
            logger.error(e.message)
            traceback.print_exc()
    return links, invalid_link_list


class Command(BaseCommand):
    def handle(self, *args, **options):
        date_str = datetime.today().strftime('%Y-%m-%d')
        total_check_link, invalid_link_list = check()
        html_content = loader.get_template('link_health.html').render(
            {
                'date_str': date_str,
                'total_check_link': total_check_link,
                'invalid_link_list': invalid_link_list,
            }
        )
        print send_mail(u'资源健康检查',message=html_content, html_message=html_content, from_email='book@loneway.ren', recipient_list=['admin@loneway.ren'])


