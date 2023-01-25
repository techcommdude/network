import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder

from yaml import serialize_all
from .models import User, Posts, Follow


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
    # TODO: most recent posts first, how to do?  Need to sort the below.
    allPosts = Posts.objects.values('id', 'creator', 'content', 'createdDate', 'numberLikes').order_by('-createdDate')

    serialized_q = json.dumps(list(allPosts), cls=DjangoJSONEncoder, default=str)
    print(serialized_q)





    # serialized_data = serialize("json", allPosts)
    # serialized_data = json.loads(serialized_data)
    # print(serialized_data)
    # test = json.dumps(serialized_data)
    # print(test)

#     createdDate = '2019-01-04T16:41:24+02:00'

#    createdDate.strftime("%b %d %Y, %I:%M %p")
    # //TODO: This converts the format of the date.
    test = datetime.datetime.fromisoformat('2019-01-04T16:41:24+02:00')
    print(test)




    # posts = json.dumps([dict(item) for item in Posts.objects.all().values('id', 'creator', 'content', 'createdDate', 'numberLikes')], default=str)
    # print(posts)

    # If you are returning anything other than a dict, you must use safe=False.
    return JsonResponse(serialized_q, safe=False, status=200)


@login_required
def getProfile(request):
    print("In getProfile")
    user = request.user

    # This returns a queryset which must be serialized to convert to JSON.
    followQS = Follow.objects.filter(followUser=user)

    serialized_data = serialize("json", followQS)
    serialized_data = json.loads(serialized_data)
    print(serialized_data)

    # TODO: Need to handle the case where nothing is returned.  What do we display on the page.

    return JsonResponse(serialized_data, safe=False, status=200)


@login_required
def getFollowing(request):
    print("In getFollowing")
    user = request.user
    print(user)

    # TODO: From the Follow object, get the "following" users and then retrieve all posts for those users with the most recent posts first.

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
