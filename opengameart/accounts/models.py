from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
    description = models.TextField()
    art_direction = models.CharField(max_length=255, choices=ART_DIRECTION, default=art)

    def __str__(self):
        """A string representation of the model."""
        current_user = User.objects.get(id=int(self.user_id))
        return current_user.username
