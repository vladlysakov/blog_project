# Generated by Django 2.2.5 on 2019-10-08 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_auto_20191008_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='time_last_logout',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='logout_time',
            field=models.DateTimeField(null=True, verbose_name='Last logout'),
        ),
    ]
