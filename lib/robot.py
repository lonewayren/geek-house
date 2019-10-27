#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'

from werobot.robot import WeRoBot as _WeRoBot, signature, six, is_regex, to_text


class BaseFilter(object):
    def __init__(self, *args, **kwargs):
        pass

    def handler(self, msg):
        return False


class WeRoBot(_WeRoBot):

    def __init__(self, *args, **kwargs):
        super(WeRoBot, self).__init__(*args, **kwargs)

    def add_filter(self, func, rules):
        """
        为 BaseRoBot 添加一个 ``filter handler``。

        :param func: 如果 rules 通过，则处理该消息的 handler。
        :param rules: 一个 list，包含要匹配的字符串或者正则表达式。
        :return: None
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))
        if not isinstance(rules, list):
            raise ValueError("{} is not list".format(rules))
        if len(rules) > 1:
            for x in rules:
                self.add_filter(func, [x])
        else:
            target_content = rules[0]
            if isinstance(target_content, six.string_types):
                target_content = to_text(target_content)

                def _check_content(message):
                    return message.content == target_content
            elif is_regex(target_content):

                def _check_content(message):
                    return target_content.match(message.content)
            elif isinstance(target_content, BaseFilter):

                def _check_content(message):
                    return bool(target_content.handler(message.content))
            else:
                raise TypeError("%s is not a valid rule" % target_content)
            argc = len(signature(func).parameters.keys())

            @self.text
            def _f(message, session=None):
                _check_result = _check_content(message)
                if _check_result:
                    if isinstance(_check_result, bool):
                        _check_result = None
                    return func(*[message, session, _check_result][:argc])
