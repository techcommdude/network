from rest_framework import routers, serializers, viewsets
from network.models import User, Posts, Follow

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','id', 'username', 'email', 'is_staff', 'is_superuser']


class FollowSerializer(serializers.ModelSerializer):
    pass

class PostSerializer(serializers.ModelSerializer):

    # TODO: This needs to be worked on.
    likedUser = UserSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-createdDate']
        model = Posts
        fields = ("url","id", "creator", "content",
                  "createdDate", "likedUser", "numberLikes")
