from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self) -> str:
        return f"User Name: {self.username} - User ID: {self.id}"


class Posts(models.Model):
    # The creator of the listing who can close it.
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator", blank=False)
    content = models.TextField(max_length=600)
    createdDate = models.DateTimeField(auto_now_add=True)
    # liked = models.BooleanField(default=False)
    #If the user liked it then above is automatically True.  If they are not in this list then they haven't liked it.
    # If the user is already in this list, then display the thumbs down.
    likedUser = models.ManyToManyField(
        User, related_name="get_liked_users", blank=True)
    #This is the total number of likes, regardless of the user.
    numberLikes = models.PositiveIntegerField(blank=True, default=0)

    # def __str__(self) -> str:
    #     return f"User: {self.creator} - user likes: {self.likedUser.all()}"


#TODO: get rid of this?
#FIXME: This is broken right now due to the additional fields. the /posts API doesn't work right now.
    def serialize(self):
        return {
            #id of the post
            "id": self.id,
            #This passes in the user id of the creator.
            "creator": getUserName(self.creator.id),
            "content": self.content,
            "createdDate": self.createdDate.strftime("%b %d %Y, %I:%M %p"),
            "likedUser": self.likedUser,
            "numberLikes": self.numberLikes
        }


class Follow(models.Model):
    #The name of the user
    followUser = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_followUser_listings", blank=False)
    #followers of the above
    followers = models.ManyToManyField(
        User, blank=True, related_name="get_follower_users")
    #Users that are being followed by above user.
    following = models.ManyToManyField(
        User, blank=True, related_name="get_following_users")


    def __str__(self) -> str:
        return f"User: {self.followUser} - Followers: {self.followers.all()} Following: {self.following.all()}"

    #TODO: get rid of this?
    def serialize(self):
        return {
            "id": self.id,
            "followUser": self.followUser,
            "followers": getFollowers(self.id),
            "following": [user.username for user in self.following.all()],
        }
def getUserName(userID):
    userName = User.objects.get(id=userID)
    test = userName.username
    #this returns the username as a string.  Not an object.
    return test

def getFollowers(id):
    #Need to loop through and return all followers.
    test = Follow.objects.filter(id=id)
    return test
