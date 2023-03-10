# Generated by Django 4.1.3 on 2023-02-06 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_posts_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='liked',
        ),
        migrations.AddField(
            model_name='posts',
            name='likedUser',
            field=models.ManyToManyField(blank=True, related_name='get_liked_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posts',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
