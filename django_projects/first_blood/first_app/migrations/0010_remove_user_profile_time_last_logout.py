# Generated by Django 2.2.6 on 2019-11-02 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_user_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='time_last_logout',
        ),
    ]