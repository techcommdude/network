
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.getProfile, name="getProfile"),
    path("following", views.getFollowing, name="getFollowing"),
    path("allPosts", views.djangoAllPosts, name="djangoAllPosts"),


    # API Routes
    path("posts", views.getAllPosts, name="getAllPosts"),
    path("posts/<int:post_id>", views.updatePost, name="updatePost"),
    path("post", views.savePost, name="savePost"),


]
