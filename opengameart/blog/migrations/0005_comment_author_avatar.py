# Generated by Django 2.0.3 on 2018-08-03 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author_avatar',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
