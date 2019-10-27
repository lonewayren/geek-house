#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from __future__ import unicode_literals
import re
import traceback

from apps.eBook.utils import search_manager
from initial import robot_instance as _robot_instance
from lib.utils import bookVerifyCodeUtils
from apps.account.serializers import WxUser
from apps.account.utils import init_wx_user
from apps.eBook.serializers import Book, Link, BookDetailSerializer
from apps.wxRobot.utils import BookTitleFilter, KeyWordsFilter, unLog

URL_MAP = {
    'book': 'https://www.loneway.ren/book/list',
    'code': 'https://mp.weixin.qq.com/mp/homepage?__biz=MzUzMjcxNTkwOQ==&hid=4&sn=806dc6b1fa037fe52a792c46f06796e7',
    'school': 'https://mp.weixin.qq.com/mp/homepage?__biz=MzUzMjcxNTkwOQ==&hid=2&sn=432f425b477fc2dde622bd21eb0f24c0',
    'society': 'https://mp.weixin.qq.com/mp/homepage?__biz=MzUzMjcxNTkwOQ==&hid=3&sn=c2ebbe8aede82ad757d1631e99433f69',
}


@_robot_instance.subscribe
def subscribe(message, session):
    welcome_msg = """欢迎你关注极客学舍。\n众人芸芸，极客寥寥。\n怀揣梦想，与你同行！\n\n专注<a href='{code}'>代码编程</a>、<a href='{book}'>经典书籍</a>\n偶有<a href='{school}'>校招内推</a>、<a href='{society}'>社招内推</a>\n希望能帮助到你。""".format(**URL_MAP)
    notice_msg = """\n注:\n    前500名用户,每人赠送1000次书籍下载机会,可回复——'我的信息'查询;回复书名可直接搜索"""
    welcome_msg += notice_msg
    try:
        # 初始化电子书信息
        openID = message.source
        try:
            user = WxUser.objects.get(id=openID)
            user.active = True
            user.save()
        except WxUser.DoesNotExist:
            # 前500用户每人送1000下载次数
            if WxUser.objects.filter(active=True).count() <= 500:
                init_wx_user(openID, '', total=1000)
            else:
                init_wx_user(openID, '')
    except Exception as e:
        traceback.print_exc()
    finally:
        return welcome_msg


@_robot_instance.unsubscribe
def unsubscribe(message, session):
    try:
        openID = message.source
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        user.active = False
        user.save()
    except Exception as e:
        traceback.print_exc()
    finally:
        return 'success'


KEYWORDS = {
    '字节跳动': 'GVXKDVN',
    '海康威视': '3S5VAR',
    '平安科技': '3X5BZ2',
    '顺丰科技': '378069',
    '搜狗': '<a href="https://app.mokahr.com/recommendation-apply/sogou-inc/3010?recommenderId=156390&hash=#/jobs?isCampusJob=1&page=1&keyword=&_k=57d305">内推链接</a>',
    '小米': '<a href="https://app.mokahr.com/m/recommendation-apply/xiaomi/3527?sharePageId=9834&recommenderId=73550&hash=%23%2Frecommendation%2Fpage%2F9834">内推链接</a>',
    '美团': '<a href="https://campus.meituan.com/bole/wechat?staffSsoId=2062479">内推链接</a>',
    '学而思': '<a href="http://neitui.info.100tal.com/share_list/?_dt_no_comment=1&code=b12699bd151fb3996ce94402f4bc6b54">内推链接</a>',
}


@_robot_instance.filter(KeyWordsFilter(keywords=KEYWORDS))
def get_school_code(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        try:
            user = WxUser.objects.get(id=message.source, active=True)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        msg = KEYWORDS[message.content]
    except Exception as e:
        msg = '获取内推信息失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.filter('验证码')
def get_book_code(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        code = bookVerifyCodeUtils.gen_verify_code(user.id)
        title = "验证码"
        description = "%s" % code
        cover = "https://www.loneway.ren/static/favicon.ico"
        link = 'https://www.loneway.ren/book'
        msg = [[title, description, cover, link]]
        msg = description
    except Exception as e:
        msg = '获取验证码失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.filter('我的信息')
def get_user_info(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        msg = """关注时间:%s\n总下载次数:%s\n已下载次数:%s\n可下载次数:%s\n""" % (user.created_time.strftime('%Y-%m-%d %H:%M:%S'), user.total, user.used, user.remain)
    except Exception as e:
        msg = '查询信息失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.filter(re.compile("^[1-9][0-9]*$"))
def get_book_info(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        book_id = message.content
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        try:
            book = Book.objects.get(id=int(book_id))
        except Book.DoesNotExist:
            msg = '{book_id}对应的书籍不存在'.format(**{'book_id': book_id})
            return
        code = bookVerifyCodeUtils.gen_verify_code(user.id)
        link = "https://www.loneway.ren/book/detail/%s?code=%s" % (book_id, code)
        msg = [[book.title, book.description, book.cover, link]]
    except Exception as e:
        msg = '获取验证码失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.filter(BookTitleFilter())
def search_book_info(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        book_name = message.content
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        try:
            book = Book.objects.filter(title__icontains=book_name).first()
        except Book.DoesNotExist:
            msg = '{book_name}对应的书籍未找到'.format(**{'book_name': book_name})
            return
        code = bookVerifyCodeUtils.gen_verify_code(user.id)
        link = "https://www.loneway.ren/book/detail/%s?code=%s" % (book.id, code)
        msg = [[book.title, book.description, book.cover, link], 'test']
    except Exception as e:
        msg = '获取验证码失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.filter(BookTitleFilter(exist=False))
def search_book_empty(message, session):
    """
    https://werobot.readthedocs.io/zh_CN/latest/messages.html
    :param message:
        {
            message_id: 消息id，64位整型
            target: 开发者账号（ OpenID ）
            source: 发送方账号（ OpenID ）
            time: 信息发送的时间，一个UNIX时间戳。
            raw: 信息的原始 XML 格式
        }
    :param session: dict
    :return:
    """
    msg = ''
    try:
        openID = message.source
        try:
            user = WxUser.objects.get(id=message.source)
        except WxUser.DoesNotExist:
            user = init_wx_user(openID, '')
        if unLog:
            msg = ''
        else:
            book_name = message.content
            search_manager.log_unhit_search(book_name, user)
            wait_member = search_manager.count_search(value=book_name)
            msg = "您搜索的书籍《{book_name}》目前尚未收录，我们会尽快收录后通知您，目前有{wait_member}人搜索该书。您可以看看<a href='https://www.loneway.ren/book'>这里</a>有没有喜欢的书籍".format(**{'book_name': book_name, 'wait_member': wait_member})
    except Exception as e:
        msg = '搜索失败'
        traceback.print_exc()
    finally:
        return msg


@_robot_instance.click
def abort(message):
    print message.key
    return "I'm a click robot"


@_robot_instance.view
def abort(message):
    print message.key
    return "I'm a view robot"


robot_instance = _robot_instance

