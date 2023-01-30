import datetime
from itertools import chain
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

#from yaml import serialize_all
from .models import User, Posts, Follow
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def savePost(request):
    # TODO: This is for saving the post when clicking the POST button at the top of the page.
    user = request.user
    userLoggedIn = request.user.username
    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    print(userName)
    print(user)
    print(userLoggedIn)

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load the content of the POST request.
    data = json.loads(request.body)
    postContent = data.get("content")

    if data.get("content") == "":
        return JsonResponse({
            "error": "You have not posted any content.  Please try again."
        }, status=400)

    newPost = Posts(
        creator=userName,
        content=postContent

    )

    newPost.save()

    return JsonResponse({"message": "Post created successfully!"}, status=201)


@csrf_exempt
@login_required
def updatePost(request, post_id):
    # TODO: This is for editing the post after clicking edit.
    print("In updatePost")

    try:
        posts = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            posts.content = data["content"]
        posts.save()

        # FIXME: Put a delay here so that the database updates.
        return HttpResponse(status=204)
    return HttpResponse("retrievePost!")


@login_required

def getAllPosts(request):

    # TODO: Keep this for the API.  Perhaps create a button or document.  /posts route.

    print("In getAllPosts")
    # TODO: most recent posts first, how to do?  Need to sort the below.

    user = User.objects.values('username')

    userName = User.objects.get(id=1)
    test = userName.username
# this is a queryset of Posts objects only
    posts = Posts.objects.all().order_by('-createdDate')

    # for post in posts:

    #     # FIXME: this only gets the last object.  Need to loop it.
    #     test = post.serialize()

    return JsonResponse([post.serialize() for post in posts], safe=False)

    # serialized_q = json.dumps(
    #     list(allPosts), cls=DjangoJSONEncoder, default=str)
    # print(serialized_q)

    # serialized_data = serialize("json", allPosts)
    # serialized_data = json.loads(serialized_data)
    # print(serialized_data)
    # test = json.dumps(serialized_data)
    # print(test)

#     createdDate = '2019-01-04T16:41:24+02:00'

#    createdDate.strftime("%b %d %Y, %I:%M %p")
    # //TODO: This converts the format of the date.
    # test = datetime.datetime.fromisoformat('2019-01-04T16:41:24+02:00')
    # print(test)

    # posts = json.dumps([dict(item) for item in Posts.objects.all().values('id', 'creator', 'content', 'createdDate', 'numberLikes')], default=str)
    # print(posts)

    # If you are returning anything other than a dict, you must use safe=False.
    # return JsonResponse(serialized_q, safe=False, status=200)

@login_required
@csrf_exempt
def djangoAllPosts(request):

    print("In DjangoAllPosts")
    # TODO: most recent posts first, how to do?  Need to sort the below.

    user = User.objects.values('username')

    userName = User.objects.get(id=1)
    test = userName.username
# this is a queryset of Posts objects only
    # postings = Posts.objects.all().order_by('-createdDate')
    postings = Posts.objects.filter().order_by('-createdDate')

    # for post in posts:

    #     # FIXME: this only gets the last object.  Need to loop it.
    #     test = post.serialize()

    return render(request, "network/allPosts.html", {"postings": postings})


@csrf_exempt
@login_required
def getProfile(request):
    print("In getProfile")
    user_id = request.user.id
    user_name= request.user.username

    currentOBJ = Follow.objects.get(id=user_id)
    #Returns querysets of User objects.
    followers = currentOBJ.followers.all()
    following = currentOBJ.following.all()

    #TODO: Possibly just combine these and then serialize?



    # This returns a queryset which must be serialized to convert to JSON.
    currentObjects = Follow.objects.filter(followUser=user_id)


    #serialized_q = json.dumps(list(currentObjects), cls=DjangoJSONEncoder)

    # return JsonResponse([currentObject.serialize() for currentObject in currentObjects], safe=False)

    return render(request, "network/profile.html", {"followers": followers, "following": following})
    # return HttpResponse("In the getProfile function!")




    # serialized_data = serialize("json", followQS)
    # serialized_data = json.loads(serialized_data)
    # print(serialized_data)

    # TODO: Need to handle the case where nothing is returned.  What do we display on the page.

    # return JsonResponse(serialized_data, safe=False, status=200)


@csrf_exempt
@login_required
def getFollowing(request):
    print("In getFollowing")
    user = request.user
    print(user)

    # TODO: From the Follow object, get the "following" users and then retrieve all posts for those users with the most recent posts first.

    return render(request, "network/following.html", {"user": user})

    #return HttpResponse("In the getFollowing function!")


@csrf_exempt
# @login_required
def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        # return render(request, "network/allPosts.html")
        return HttpResponseRedirect(reverse("djangoAllPosts"))


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
