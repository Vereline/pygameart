# Generated by Django 2.0.3 on 2018-07-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_artpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='artuser',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]