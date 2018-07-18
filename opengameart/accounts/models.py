from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from arts.models import Art

# Create your models here.
image_storage = FileSystemStorage(
    # Physical file location ROOT
    location='{0}/images/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url='{0}images/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/avatars/<filename>
    return 'avatars/{0}'.format(filename)


class ArtUser(models.Model):
    art = 'ART'
    music = 'MUS'
    video = 'VID'
    text = 'TXT'
    ART_DIRECTION = (
        (art, 'Art'),
        (music, 'Music'),
        (video, 'Video'),
        (text, 'Text'),
    )

    user_id = models.CharField(default="", max_length=255)
    location = models.CharField(max_length=255, default="", null=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    art_direction = models.CharField(max_length=255, choices=ART_DIRECTION, default=art)
    user_avatar = models.ImageField(upload_to=image_directory_path, storage=image_storage, null=True, blank=True)
    liked_arts = models.ManyToManyField(Art)

    def __str__(self):
        """A string representation of the model."""
        current_user = User.objects.get(id=int(self.user_id))
        return current_user.username

    def save(self, update_picture=False, *args, **kwargs):
        """ Save Art model."""
        try:
            if update_picture:
                file_name = self.user_avatar.name
                art_user_id = get_id_by_path(file_name)
                file_name = file_name.split('.')
                # Rename image file into unique value
                self.file_id = art_user_id
                self.user_avatar.name = self.file_id + '.' + file_name[-1]

        except Exception as e:
            print("Error trying to save model: saving image failed: " + str(e))
            pass

        super(ArtUser, self).save(*args, **kwargs)

    def get_user_info(self):
        return User.objects.get(id=int(self.user_id)).__dict__

    def get_username(self):
        return self.get_user_info()['username']


def get_id_by_path(file_path):
    import hashlib
    import datetime
    str_to_encode = file_path + str(datetime.datetime.now().date())
    art_id = None
    try:
        art_id = hashlib.md5(str_to_encode.encode()).hexdigest()
    except Exception as e:
        print('{}, {}'.format(type(e), e))
    return art_id


class ArtPost(models.Model):
    user = models.ForeignKey(ArtUser, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        title = self.art.title
        author = User.objects.get(id=int(self.user.user_id)).username
        return '{author}: {title}'.format(title=title, author=author)

# add later models for TxtPost, MusicPost, etc
