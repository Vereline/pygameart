from django.contrib import admin
from .models import ArtUser, ArtPost, Relationship
# Register your models here.
from django.utils.html import mark_safe
from opengameart.settings import STATIC_URL


class LikedArtsInline(admin.TabularInline):
    model = ArtUser.liked_arts.through


class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_person'


class ArtUserAdmin(admin.ModelAdmin):
    model = ArtUser
    list_display = ('user_id', 'location', 'birth_date', 'art_direction', 'id')
    fields = ('__str__', 'user_id', 'user_avatar', 'display_image_field',  'location', 'birth_date',
              'art_direction', 'description')
    readonly_fields = ['__str__', 'display_image_field']
    inlines = [LikedArtsInline, RelationshipInline]

    def display_image_field(self, obj):
        if obj.user_avatar:
            url = obj.user_avatar.url
            if not self.check_image_path(url):
                self.fix_images_paths()
        else:
            url = STATIC_URL + 'user-default.png'
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=url,
            width=300,
            height=300,
        )
        )

    def fix_images_paths(self):
        all_users = [user for user in ArtUser.objects.all()]
        for user in all_users:
            if user.user_avatar:
                image_path = user.user_avatar.url
                if not self.check_image_path(image_path):
                    dirs_arr = user.user_avatar.url.split('/')
                    dirs_arr.insert(-1, 'avatars')
                    dirs_arr = '/'.join(dirs_arr)
                    user.user_avatar.url = dirs_arr
                    user.save(update_picture=False)

    @staticmethod
    def check_image_path(path):
        if '/avatars/' not in path:
            return False
        return True


class ArtPostAdmin(admin.ModelAdmin):
    model = ArtPost


class ArtRelationshipAdmin(admin.ModelAdmin):
    model = Relationship


admin.site.register(ArtUser, ArtUserAdmin)
admin.site.register(ArtPost, ArtPostAdmin)
admin.site.register(Relationship, ArtRelationshipAdmin)


