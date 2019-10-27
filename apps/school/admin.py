# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from .models import Work, Company


class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'href', 'hot', 'start_time', 'end_time', 'company')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo')

admin.site.register(Work, WorkAdmin)
admin.site.register(Company, CompanyAdmin)
