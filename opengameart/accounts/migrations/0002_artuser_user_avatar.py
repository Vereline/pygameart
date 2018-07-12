# Generated by Django 2.0.3 on 2018-07-10 11:38

import accounts.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artuser',
            name='user_avatar',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/images/', location='/home/wsc-194a/workspace/OpenGameArt/opengameart/media/images/'), upload_to=accounts.models.image_directory_path),
        ),
    ]