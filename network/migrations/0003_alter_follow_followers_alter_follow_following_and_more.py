# Generated by Django 4.1.3 on 2023-01-26 20:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_follow_followers_remove_follow_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='get_follower_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='get_following_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=models.TextField(max_length=600),
        ),
    ]
