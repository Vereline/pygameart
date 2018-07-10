from django.contrib import admin
from .models import ArtUser
# Register your models here.


class ArtUserAdmin(admin.ModelAdmin):
    model = ArtUser
    list_display = ('user_id', 'location', 'art_direction')
    fields = ('__str__', 'user_id', 'location', 'art_direction', 'description')
    readonly_fields = ['__str__']


admin.site.register(ArtUser, ArtUserAdmin)
