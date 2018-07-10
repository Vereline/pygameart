from django.contrib import admin
from .models import ArtUser
# Register your models here.
from django.utils.html import mark_safe


class ArtUserAdmin(admin.ModelAdmin):
    model = ArtUser
    list_display = ('user_id', 'location', 'art_direction')
    fields = ('__str__', 'user_id', 'user_avatar', 'display_image_field',  'location', 'art_direction', 'description')
    readonly_fields = ['__str__', 'display_image_field']

    def display_image_field(self, obj):
        url = obj.user_avatar.url
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=url,
            width=300,
            height=300,
        )
        )


admin.site.register(ArtUser, ArtUserAdmin)
