from django.db import models
from PIL import Image  # Holds downloaded image and verifies it
import copy  # Copies instances of Image
# Create your models here.


class Art(models.Model):
    file_id = models.CharField(unique=True, max_length=100, default='')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.CharField(max_length=255)
    file = models.ImageField(upload_to='images/loaded/', null=True, blank=True)
    # file = models.ImageField(upload_to=os.path.join(BASE_DIR, 'images/loaded/'), null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        """A string representation of the model."""
        return self.title

    def save(self, *args, **kwargs):
        """ Save Art model."""
        file_name = self.file.name
        try:
            img = Image.open(self.file)  # Creates an instance of PIL Image class - PIL does the verification of file

            # img_copy = copy.copy(img)
            # if not valid_img(img_copy):
            #     raise Exception('An invalid image was detected when attempting to save an Art!')

            art_id = get_id_by_path(file_name)
            file_name = file_name.split('.')
            # Rename image file into unique value
            self.file_id = art_id
            self.file.name = self.file_id + '.' + file_name[-1]
            self.file_path = 'images/loaded/' + self.file.name

        except Exception as e:
            print("Error trying to save model: saving image failed: " + str(e))
            pass

        super(Art, self).save(*args, **kwargs)


def valid_img(img):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    img_type = img.format
    if img_type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except Exception as e:
            print(e)
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
    except Exception as e:
        print('{}, {}'.format(type(e), e))
    return art_id
