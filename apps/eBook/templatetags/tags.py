#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'
from django.urls import reverse
from django import template

register = template.Library()


@register.inclusion_tag('html/index.html')
def load_pagination_info(page_obj, page_type, tag_name):
    previous_url = ''
    next_url = ''
    print page_obj, page_type, tag_name, 123
    if page_type == '':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = "%s?page=%s" % (reverse('apps.eBook.BookListHtml'), next_number)
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = "%s?page=%s" % (reverse('apps.eBook.BookListHtml'), previous_number)
    return {
        'previous_url': previous_url,
        'next_url': next_url,
        'page_obj': page_obj
    }