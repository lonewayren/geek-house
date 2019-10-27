# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from .models import Work


# Register your models here.
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'href', 'hot', 'start_time', 'end_time')


admin.site.register(Work, WorkAdmin)
