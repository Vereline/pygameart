from django.contrib.auth.models import User
from django.test import TestCase
from .models import Art
from accounts.models import ArtUser
import os
from django.test import Client
# Create your tests here.


class ArtViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_user')
        user.set_password('12345abc')
        user.save()

        ArtUser.objects.create(user_id=str(user.id))

        user = User.objects.create_superuser(username='test_superuser')
        user.set_password('super12345abc')
        user.save()

        ArtUser.objects.create(user_id=str(user.id))

        Art.objects.create(title='first todo', file='arts/test_art/1.ico', file_id='1', likes=1)
        Art.objects.create(description='a description here', file='arts/test_art/2.ico', file_id='2', owner_id='1')

    def test_art_creation(self):
        client = Client()
        log_in = client.login(username='test_user', passwor='12345abc')
        super_client = Client()
        log_in_super = super_client.login(username='test_superuser', passwor='super12345abc')


    @classmethod
    def tearDownTestData(cls):
        art = Art.objects.get(id=1)
        file_path = art.file_path
        os.remove(file_path)

        art = Art.objects.get(id=2)
        file_path = art.file_path
        os.remove(file_path)
