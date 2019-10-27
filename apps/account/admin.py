# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from .models import WxUser


# Register your models here.
class WxUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_time', 'last_mod_time', 'active', 'used', 'total')


admin.site.register(WxUser, WxUserAdmin)
