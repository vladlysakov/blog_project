# Generated by Django 2.2.5 on 2019-10-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='articles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='first_app.Article'),
        ),
    ]
