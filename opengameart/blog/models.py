from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

# Create your models here.
image_storage = FileSystemStorage(
    # Physical file location ROOT
    location='{0}/images/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url='{0}images/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/avatars/<filename>
    return 'news/{0}'.format(filename)


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    post_image = models.ImageField(upload_to=image_directory_path, storage=image_storage, null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    author_id = models.CharField(max_length=200, default='', blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
