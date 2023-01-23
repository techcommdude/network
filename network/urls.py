
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API Routes
    path("posts", views.getAllPosts, name="getAllPosts"),
    path("posts/<int:post_id>", views.retrievePost, name="retrievePost"),
    path("profile", views.getProfile, name="getProfile"),
    path("following", views.getFollowing, name="getFollowing"),

]
