# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from .models import Book, Link, Source, Category, Search


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'cover', 'description')
    search_fields = ('id', 'title')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'link', 'type', 'secret', 'valid')
    search_fields = ('id', 'book__title')
    list_filter = ('valid',)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'host')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'user')


admin.site.register(Search, SearchAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Category, CategoryAdmin)
