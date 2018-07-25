from django.contrib import admin
from django.utils.safestring import mark_safe

from opengameart.settings import STATIC_URL
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('author', 'title', 'created_date', 'published_date')
    fields = ('author', 'title', 'created_date', 'published_date', 'text', 'post_image', 'display_image_field')
    readonly_fields = ['display_image_field']

    def display_image_field(self, obj):
        if obj.post_image:
            url = obj.post_image.url
        else:
            url = STATIC_URL + 'user-default.png'
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=url,
            width=300,
            height=300,
        )
        )


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('author', 'created_date')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
