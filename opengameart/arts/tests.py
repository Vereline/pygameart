from django.test import TestCase
from .models import Art
from accounts.models import ArtUser
import os
# Create your tests here.


class ArtModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Art.objects.create(title='first todo', file='arts/test_art/1.ico', file_id='1', likes=1)
        ArtUser.objects.create(user_id='111')
        Art.objects.create(description='a description here', file='arts/test_art/2.ico', file_id='2', owner_id='1')

    def test_title_content(self):
        art = Art.objects.get(id=1)
        expected_object_name = '{title}'.format(title=art.title)
        self.assertEquals(expected_object_name, 'first todo')

    def test_likes(self):
        art = Art.objects.get(id=1)
        expected_object_likes = art.likes
        self.assertEquals(expected_object_likes, 1)
        second_art = Art.objects.get(id=2)
        expected_likes_second = second_art.likes
        self.assertEquals(expected_likes_second, 0)

    def test_description_content(self):
        art = Art.objects.get(id=2)
        expected_object_name = '{description}'.format(description=art.description)
        self.assertEquals(expected_object_name, 'a description here')

    def test_art_image(self):
        # TODO: implement this test
        pass

    def test_owner_id(self):
        art = Art.objects.get(id=2)
        user = ArtUser.objects.get(id=1)
        art_owner = int(art.owner_id)
        self.assertEqual(art_owner, user.id)

    @classmethod
    def tearDownTestData(cls):
        art = Art.objects.get(id=1)
        file_path = art.file_path
        os.remove(file_path)

        art = Art.objects.get(id=2)
        file_path = art.file_path
        os.remove(file_path)

