from django.contrib import admin
from . import models

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'status')

admin.site.register(models.Post, AuthorAdmin)

