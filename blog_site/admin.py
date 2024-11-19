import os

from django.contrib import admin
from .models import Post, Comment




class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)