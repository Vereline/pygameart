from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('author', 'title', 'created_date', 'published_date')


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('author', 'created_date')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
