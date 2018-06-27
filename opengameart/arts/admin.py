from django.contrib import admin

# Register your models here.
from .models import Art
from django.utils.html import mark_safe
from opengameart.settings import MEDIA_ROOT, MEDIA_URL
import os


class ArtAdmin(admin.ModelAdmin):
    model = Art
    list_display = ('title', 'file_id', 'id', 'file_path', 'likes', 'creation_date')
    fields = ('title', 'description', 'file', 'display_image_field', 'likes')
    readonly_fields = ['display_image_field']

    def display_image_field(self, obj):
        # print(os.getcwd())
        url = os.getcwd() + obj.file.url
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=url,
            width=300,
            height=300,
        )
        )


admin.site.register(Art, ArtAdmin)
