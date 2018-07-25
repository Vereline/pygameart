from django.db import models

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    country = models.CharField(max_length=255)
    subject_text = models.TextField()

    def __str__(self):
        return self.first_name
