from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self) -> str:
        return f"User Name: {self.username} - User ID: {self.id}"


class Posts(models.Model):
    # The creator of the listing who can close it.
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator_listings", blank=False)
    content = models.CharField(max_length=600)
    createdDate = models.DateTimeField(auto_now_add=True)
    numberLikes = models.IntegerField(blank=True, default=0)

#TODO: get rid of this?
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator,
            "content": self.content,
            "createdDate": self.createdDate.strftime("%b %d %Y, %I:%M %p"),
            "numberLikes": self.numberLikes,
        }


class Follow(models.Model):
    followUser = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_followUser_listings", blank=False)
    followers = models.ManyToManyField(
        User, blank=True, related_name="get_follower_users")
    following = models.ManyToManyField(
        User, blank=True, related_name="get_following_users")

    def __str__(self) -> str:
        return f"ID: {self.id} - User: {self.followUser} - Followers: {self.followers.all()} Following: {self.following.all()}"

    #TODO: get rid of this?
    def serialize(self):
        return {
            "id": self.id,
            "followUser": self.followUser,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
        }
