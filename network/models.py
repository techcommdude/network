from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    # The creator of the listing who can close it.
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator_listings", blank=False)
    content = models.CharField(max_length=600)
    createdDate = models.DateTimeField(auto_now_add=True)
    numberLikes = models.IntegerField(blank=True, default=0)


class Follow(models.Model):
    followers = models.ManyToManyField(
        User, blank=True, related_name="get_follower_posts")
    following = models.ManyToManyField(
        User, blank=True, related_name="get_following_posts")
