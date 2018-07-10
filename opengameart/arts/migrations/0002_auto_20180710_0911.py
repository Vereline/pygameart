# Generated by Django 2.0.3 on 2018-07-10 09:11

import arts.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='file',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/images/', location='/home/wsc-194a/workspace/OpenGameArt/opengameart/media/images/'), upload_to=arts.models.image_directory_path),
        ),
    ]
