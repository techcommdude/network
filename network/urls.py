
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user_Follow/<str:username>", views.user_Follow, name="user_Follow"),
    path("user_UnFollow/<str:username>", views.user_UnFollow, name="user_UnFollow"),
    path("profile/<str:username>", views.getProfile, name="getProfile"),
    path("following", views.getFollowing, name="getFollowing"),
    path("allPosts", views.djangoAllPosts, name="djangoAllPosts"),
    path("newPost", views.saveDjangoNewPost, name="saveDjangoNewPost"),


    # API Routes
    path("posts", views.getAllPosts, name="getAllPosts"),
    path("posts/<int:post_id>", views.updatePost, name="updatePost"),
    path("post", views.savePost, name="savePost"),


]
