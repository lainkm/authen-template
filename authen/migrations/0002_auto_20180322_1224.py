# Generated by Django 2.0.3 on 2018-03-22 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='nick_name',
            new_name='nickname',
        ),
    ]
