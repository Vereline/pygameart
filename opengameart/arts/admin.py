from django.contrib import admin

# Register your models here.
from .models import Art, ArtComment
from django.utils.html import mark_safe


class ArtAdmin(admin.ModelAdmin):
    model = Art
    list_display = ('title', 'file_id', 'id', 'file_path', 'likes', 'creation_date', 'owner_id')
    fields = ('title', 'description', 'file', 'display_image_field', 'likes', 'owner_id')
    readonly_fields = ['display_image_field']

    def display_image_field(self, obj):
        url = obj.file.url
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=url,
            width=300,
            height=300,
        )
        )


class ArtCommentAdmin(admin.ModelAdmin):
    model = ArtComment
    list_display = ('author', 'created_date')


admin.site.register(ArtComment, ArtCommentAdmin)
admin.site.register(Art, ArtAdmin)
