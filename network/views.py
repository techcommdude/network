import datetime
from itertools import chain
import time
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
    # TODO: Use this to return the JSON for a particular post.
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


def saveDjangoNewPost(request):
    # TODO: This is for saving the post when clicking the POST button at the top of the page.
    user = request.user
    userLoggedIn = request.user.username
    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    print(userName)
    print(user)
    print(userLoggedIn)

    if request.method == "POST":

        postContent = request.POST.get("postContent")

    # //Need to issue an error message here.
    if request.POST.get("postContent") == "":
        # FIXME: Return an error message at this point.
        return HttpResponse("Nothing in your Post!")

    newPost = Posts(
        creator=userName,
        content=postContent
    )

    newPost.save()
    return HttpResponseRedirect(reverse("djangoAllPosts"))


@csrf_exempt
@login_required
def updatePost(request, post_id):

    # TODO: This is for editing the post after clicking edit.
    print("In updatePost")

    # TODO: Use this to return the JSON for a particular post.
    # user = request.user
    # userLoggedIn = request.user.username
    # Get the user ID of the logged in user for the User object
    # user_id = request.user.id
    # userName = User.objects.get(id=user_id)
    # print(userName)
    # print(user)
    # print(userLoggedIn)

    # try:
    #     test = Posts.objects.get(pk=post_id)
    # except Posts.DoesNotExist:
    #     return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":

        data = json.loads(request.body)
        # FIXME: This is where teh webpage changes for some reason.
        post = Posts.objects.get(pk=post_id)
        if data.get("content") is not None:
            post.content = data["content"]

            post.save()

            post = Posts.objects.get(pk=post_id)

            # FIXME: Put a delay here

            time.sleep(1.0)

            # return HttpResponseRedirect(reverse("djangoAllPosts"))

        # FIXME: Put a delay here so that the database updates.
    return HttpResponse(status=204)
    # return HttpResponse("retrievePost!")


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

    #user = User.objects.values('username')

    # userName = User.objects.get(id=1)
    # test = userName.username
# this is a queryset of Posts objects only
    # postings = Posts.objects.all().order_by('-createdDate')
    postings = Posts.objects.filter().order_by('-createdDate')

    # for post in posts:

    #     # FIXME: this only gets the last object.  Need to loop it.
    #     test = post.serialize()

    return render(request, "network/allPosts.html", {"postings": postings})


@csrf_exempt
@login_required
def getProfile(request, username):
    print("In getProfile")
    # Information for the logged in user.  Not really relevant for the most part.
    # if the logged in user is different then link clicked user, then display the folllow and  unfollow buttons.
    user_id = request.user.id
    user_name = request.user.username

    # Information of the user that we need to retrieve posts for.
    print(username)
    user = User.objects.get(username=username)
    print(user.id)
    profileUser = user.id

    # FIXME: Need to think about clicking on links and  on the title bar.  there is a difference.

    # All of the listings we need to display in the profile page.
    # Need to check for empty queryset.  Doesnotexist error.

    try:
        postsUser = Posts.objects.filter(creator=profileUser)
    except Posts.DoesNotExist:
        print("blah")

    # Need to pass a value if the user has no postings.

    # Returns querysets of User objects.

    noListings = False
    try:
        follow = Follow.objects.get(followUser=profileUser)
    except:
        Follow.DoesNotExist
        noListings = True
        follow = False

    if postsUser:

        followers = follow.followers.all()
        following = follow.following.all()

    countFollowers = 0
    countFollowing = 0

#FIXME: error here for no listings and no followers.
    if follow != False:

        if followers:
            countFollowers = follow.followers.all().count()
        if following:
            countFollowing = follow.following.all().count()

    if follow == False:
        #This one does not return the users that are following and followers.  May or may not use that.
        return render(request, "network/profile.html", {"noListings": noListings,"postings": postsUser, "countFollowers": countFollowers, "countFollowing": countFollowing, "username": username})
    else:
        return render(request, "network/profile.html", {"noListings": noListings,"postings": postsUser, "followers": followers, "following": following, "countFollowers": countFollowers, "countFollowing": countFollowing, "username": username})





    # This returns a queryset which must be serialized to convert to JSON.
    # currentObjects = Follow.objects.filter(followUser=user_id)

    #serialized_q = json.dumps(list(currentObjects), cls=DjangoJSONEncoder)

    # return JsonResponse([currentObject.serialize() for currentObject in currentObjects], safe=False)

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

    user_id = request.user.id
    user_name = request.user.username

    #FIXME: If the user doesnlt have any followers, following or posts it will throw an error.

    try:
        currentOBJ = Follow.objects.get(id=user_id)
    except Follow.DoesNotExist:
        print("This user follows no one!")
        displayNothing = True

    if displayNothing != True:


        following = currentOBJ.following.all()

        qs = following.order_by().values('id')

        qs = list(qs)

        # //Empty queryset.
        emptyQueryset = Posts.objects.filter(creator=0)
        for dic in qs:
            for val in dic.values():
                print(val)
                listings = Posts.objects.filter(creator=val)
                UserObject = User.objects.filter(id=val)

                # Merge the queryset with the existing queryset with the new queryset.
                # If the queryset is not empty.
                if emptyQueryset.exists():
                    newQueryset = newQueryset | listings

                else:

                    newQueryset = emptyQueryset | listings
                    emptyQueryset = newQueryset

    # Sort by created date.
        PostsByDate = newQueryset.order_by('-createdDate')

        return render(request, "network/following.html", {"listings": PostsByDate, "UserObject": UserObject, "displayNothing": displayNothing,})

    else:

        return render(request, "network/following.html", {"displayNothing": displayNothing})



def appendQueryset(postings):

    s1 = Posts.objects.filter(creator=0)


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
