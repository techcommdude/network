from rest_framework import routers, serializers, viewsets
from network.models import User, Posts, Follow

# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class FollowSerializer(serializers.ModelSerializer):
     pass
class PostSerializer(serializers.ModelSerializer):

    #TODO: This needs to be worked on.
        get_liked_users = UserSerializer(many=True, read_only=True)

        class Meta:
            ordering = ['-createdDate']
            model = Posts
            fields = ("id", "creator", "content", "createdDate", "get_liked_users", "numberLikes")
            #TODO: This never shows anything.
            # extra_kwargs = {'get_liked_users': {'required': True}}