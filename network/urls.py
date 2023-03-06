
from django.urls import include, path

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # No JavaScript for this one.  Purely Django and Python.
    path("follow/<str:username>", views.follow, name="follow"),
    # JavaScript Follow/Unfollow button
    path("followUser/<str:username>", views.followUser, name="followUser"),
    path("profile/<str:username>", views.getProfile, name="getProfile"),
    path("following", views.getFollowing, name="getFollowing"),
    # Displays All posts and requires a complete refresh of the page.  Never called from JS.
    path("allPosts", views.djangoAllPosts, name="djangoAllPosts"),
    # Saving a NEW post at the top of the page.  No JS involved.
    path("newPost", views.saveDjangoNewPost, name="saveDjangoNewPost"),
    # Javascript no refresh of page for liking and unliking a Post.
    path("likePost/<int:postID>", views.likePost, name="likePost"),
    path("unlikePost/<int:postID>", views.unlikePost, name="unlikePost"),
    # This is for editing the post after clicking the edit button.
    path("posts/<int:post_id>", views.getPost, name="getPost"),

    # API Routes
    # This is never called in JavaScript or from any HTML page.  Need to redo this for the API.  A GET  for all posts.
    # path("posts", views.getAllPosts, name="getAllPosts"),
    path("post", views.savePost, name="savePost"),


]
