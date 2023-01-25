# Generated by Django 4.1.3 on 2023-01-24 09:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='get_follower_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='get_following_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]