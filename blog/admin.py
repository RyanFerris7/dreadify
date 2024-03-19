from django.contrib import admin
from . import models
from .models import QuillPost

# Register your models here.

@admin.register(QuillPost)
class QuillPostAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'status')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content')

class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'thumbs_up_count', 'thumbs_down_count')

admin.site.register(models.Post, AuthorAdmin)
admin.site.register(models.Comments, CommentsAdmin)
admin.site.register(models.Poll, PollAdmin)
admin.site.register(models.Article, QuillPostAdmin)


