# Generated by Django 2.0.3 on 2018-07-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arts', '0003_art_owner_id'),
        ('accounts', '0004_artuser_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='artuser',
            name='liked_arts',
            field=models.ManyToManyField(to='arts.Art'),
        ),
    ]
