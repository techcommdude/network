
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #No JavaScript for this one.  Purely Django and Python.
    path("follow/<str:username>", views.follow, name="follow"),
    #JavaScript Follow/Unfollow button
    path("followUser/<str:username>", views.followUser, name="followUser"),
    path("profile/<str:username>", views.getProfile, name="getProfile"),
    path("following", views.getFollowing, name="getFollowing"),
    path("allPosts", views.djangoAllPosts, name="djangoAllPosts"),
    path("newPost", views.saveDjangoNewPost, name="saveDjangoNewPost"),
    path("likePost/<int:postID>", views.likePost, name="likePost"),
    path("unlikePost/<int:postID>", views.unlikePost, name="unlikePost"),


    # API Routes
    path("posts", views.getAllPosts, name="getAllPosts"),
    path("posts/<int:post_id>", views.updatePost, name="updatePost"),
    path("post", views.savePost, name="savePost"),


]
