import logging
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image  # Holds downloaded image and verifies it
import copy  # Copies instances of Image
# Create your models here.


logger = logging.getLogger(__name__)


image_storage = FileSystemStorage(
    # Physical file location ROOT
    location='{0}/images/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url='{0}images/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/loaded/<filename>
    return 'loaded/{0}'.format(filename)


class Art(models.Model):
    file_id = models.CharField(unique=True, max_length=100, default='')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.CharField(max_length=255)
    file = models.ImageField(upload_to=image_directory_path, storage=image_storage, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    owner_id = models.CharField(default="", max_length=255)

    def __str__(self):
        """A string representation of the model."""
        return self.title

    def save(self, update_picture=False, *args, **kwargs):
        """ Save Art model."""
        try:
            if update_picture:
                file_name = self.file.name
                # Creates an instance of PIL Image class - PIL does the verification of file
                img = Image.open(self.file)
                # img_copy = copy.copy(img)
                # if not valid_img(img_copy):
                #     raise Exception('An invalid image was detected when attempting to save an Art!')

                art_id = get_id_by_path(file_name)
                file_name = file_name.split('.')
                # Rename image file into unique value
                self.file_id = art_id
                self.file.name = self.file_id + '.' + file_name[-1]
                self.file_path = '/images/loaded/' + self.file.name
                logging.info('Created unique file name ' + art_id)

        except Exception as ex:
            logger.error("Error trying to save model: saving image failed: " + str(ex))
            pass

        super(Art, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Art, self).delete(*args, **kwargs)


def valid_img(img):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    img_type = img.format
    if img_type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except Exception as ex:
            logger.error(ex)
            return False
    else:
        return False


def get_id_by_path(file_path):
    import hashlib
    import datetime
    str_to_encode = file_path + str(datetime.datetime.now())
    art_id = None
    try:
        art_id = hashlib.md5(str_to_encode.encode()).hexdigest()
    except Exception as ex:
        logger.error('{}, {}'.format(type(ex), ex))
    return art_id
