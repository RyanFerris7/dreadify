from django.contrib import admin
from . import models

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'status')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content')

class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbs_up_count', 'thumbs_down_count')

admin.site.register(models.Post, AuthorAdmin)
admin.site.register(models.Comments, CommentsAdmin)
admin.site.register(models.Poll, PollAdmin)


