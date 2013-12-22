__author__ = 'indieman'

from django.contrib import admin
from models import Hashtag, Post


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'created', 'text', 'hashtags')
    filter_horizontal = ('hashtags',)


class HashtagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Post, PostAdmin)