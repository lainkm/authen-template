# Generated by Django 2.0.3 on 2018-03-25 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0002_auto_20180322_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['-date_joined'], 'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='resume',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='简介'),
        ),
    ]
