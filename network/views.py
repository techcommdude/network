from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, Posts


@login_required
def savePost(request):
    user = request.user
    print(user)
    return HttpResponse("savePOST!")

@login_required
def retrievePost(request, post_id):
    # TODO: This is for editing the post after clicking edit.
    print("In retrievePost")
    return HttpResponse("retrievePost!")

@login_required
def getAllPosts(request):

    print("In getAllPosts")
    #Need default = str to convert the datetime object to a string.
    posts = json.dumps([dict(item) for item in Posts.objects.all().values('id', 'creator', 'content', 'createdDate', 'numberLikes')], default=str)

    #If you are returning anything other than a dict, you must use safe=False.
    return JsonResponse(posts, safe=False)

@login_required
def getProfile(request):
    print("In getProfile")
    user = request.user
    print(user)
    return HttpResponse("getProfile!")

@login_required
def getFollowing(request):
    print("In getFollowing")
    user = request.user
    print(user)
    return HttpResponse("getFollowing!")


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "network/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="500.html"):
    response = render(template_name)
    response.status_code = 500
    return response
