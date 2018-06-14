from django.contrib import admin

# Register your models here.
from .models import Art


class ArtAdmin(admin.ModelAdmin):
    model = Art
    list_display = ('title', 'id', 'file_path', 'likes', 'creation_date')
    fields = ('title', 'description', 'file', 'likes')


admin.site.register(Art, ArtAdmin)
