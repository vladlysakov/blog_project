# Generated by Django 2.2.5 on 2019-10-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_auto_20191001_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='logout_time',
            field=models.DateTimeField(null=True, verbose_name='Last cativity'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='session_time',
            field=models.DateTimeField(null=True, verbose_name='Active time'),
        ),
    ]
