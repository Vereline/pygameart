# Generated by Django 2.0.3 on 2018-07-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=255)),
                ('location', models.CharField(default='', max_length=255, null=True)),
                ('description', models.TextField()),
                ('art_direction', models.CharField(choices=[('ART', 'Art'), ('MUS', 'Music'), ('VID', 'Video'), ('TXT', 'Text')], default='ART', max_length=255)),
            ],
        ),
    ]