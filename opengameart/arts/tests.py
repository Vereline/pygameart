from django.test import TestCase
from .models import Art
import os
# Create your tests here.


class ArtModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Art.objects.create(title='first todo', file='arts/test_art/1.ico')
        Art.objects.create(description='a description here', file='arts/test_art/2.ico')

    def test_title_content(self):
        art = Art.objects.get(id=1)
        expected_object_name = '{title}'.format(title=art.title)
        self.assertEquals(expected_object_name, 'first todo')

    def test_description_content(self):
        art = Art.objects.get(id=2)
        expected_object_name = '{description}'.format(description=art.description)
        self.assertEquals(expected_object_name, 'a description here')

    @classmethod
    def tearDownTestData(cls):
        art = Art.objects.get(id=1)
        file_path = art.file_path
        os.remove(file_path)

        art = Art.objects.get(id=2)
        file_path = art.file_path
        os.remove(file_path)
