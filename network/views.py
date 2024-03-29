from rest_framework import routers, serializers, viewsets, status
import datetime
from itertools import chain
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder
from yaml import serialize_all

from network.serializers import PostSerializer, FollowSerializer, UserSerializer

from .models import User, Posts, Follow
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


@login_required
def likePost(request, postID):
    test = postID
    print(test)

    # user id and username of the logged in user.
    user_id = request.user.id
    user_name = request.user.username
    userName = User.objects.get(id=user_id)

    # Need to increase the Like count for this post.  Add the user to the likedUser field of the Post.

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if request.method == "PUT":

        data = json.loads(request.body)
        # FIXME: This is where teh webpage changes for some reason.
        post = Posts.objects.get(pk=postID)

        post.numberLikes = post.numberLikes + 1

        post.save()

        # Add a new field to the data dictionary that needs to be returned in the JSON response.
        data['numberLikes'] = post.numberLikes
        print(data)

        # Also need to remove the user from the likedUser field if it exists.
        likedUserList = post.likedUser.all()

        if userName not in likedUserList:
            post.likedUser.add(user_id)
            post.save()
            print(post.likedUser.all())

    return JsonResponse({"data": data["numberLikes"]}, safe=False)


@login_required
def unlikePost(request, postID):
    test = postID
    print(test)

    # user id and username of the logged in user.
    user_id = request.user.id
    user_name = request.user.username
    userName = User.objects.get(id=user_id)

    # Need to decrease the Like count for this post.  Remove the user from the likedUser field of the Post.

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if request.method == "PUT":

        data = json.loads(request.body)
        # FIXME: This is where teh webpage changes for some reason.
        post = Posts.objects.get(pk=postID)

        if post.numberLikes != 0:
            post.numberLikes = post.numberLikes - 1

            post.save()

           # Add a new field to the data dictionary that needs to be returned in the JSON response.
            data['numberLikes'] = post.numberLikes
            print(data)

        # Also need to remove the user from the likedUser field if it exists.
        likedUserList = post.likedUser.all()

        if userName in likedUserList:
            post.likedUser.remove(user_id)
            post.save()
            print(post.likedUser.all())

    return JsonResponse({"data": data["numberLikes"]}, safe=False)


@login_required
def saveDjangoNewPost(request):
    # This is for saving the post when clicking the POST button at the top of the page.
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

    # //This is validated on the front end, so no longer necessary.  Should never happen.
    if request.POST.get("postContent") == "":
        # FIXME: Return an error message at this point.
        # return HttpResponse("Nothing in your Post!")

        messages.error(
            request, 'You cannot submit an empty post. Please try again.')
        # Redirect to activeListings page.
        return HttpResponseRedirect(reverse("index"))

    newPost = Posts(
        creator=userName,
        content=postContent
    )

    newPost.save()
    messages.info(
        request, 'Your post has been submitted.')
    return HttpResponseRedirect(reverse("djangoAllPosts"))


@login_required
def getPost(request, post_id):

    # TODO: This is for editing the post after clicking edit.
    print("In getPost")

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if request.method == "PUT":

        data = json.loads(request.body)

        # FIXME: Can do an ID of 107-80 for the ID.
        # TODO: Need to account for DoesNotExist error if they type an ID that does not exist.

        try:
            post = Posts.objects.get(pk=post_id)
        except Posts.DoesNotExist:
            # return JsonResponse({"error": "Post not found."}, status=404)
            messages.error(
                request, 'Post with ID of ' + str(post_id) + ' not found.  Please try again.')
        # Redirect to activeListings page.
            return HttpResponseRedirect(reverse("index"))

        if data.get("content") is not None:
            postContent = data["content"]

            post.content = postContent
            post.save()
            time.sleep(0.5)

            return JsonResponse({"message": "Post created successfully!", "data": data["content"]}, safe=False)


# ViewSets define the view behavior.
@extend_schema(description='API endpoint that lists all posts for all users.', methods=["GET"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["POST"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PUT"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PATCH"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["DELETE"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post']

@extend_schema(description='API endpoint that lists all Follow objects for all users.', methods=["GET"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["POST"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PUT"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PATCH"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["DELETE"])
class FollowViewSet(viewsets.ModelViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    http_method_names = ['get']


@extend_schema(description='API endpoint that lists all users.', methods=["GET"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["POST"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PUT"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["PATCH"])
@extend_schema(description='This API endpoint is not implemented.  Please do not use.', methods=["DELETE"])
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete']


# Used by the Django Paginator class

class PostsListView(ListView):
    model = Posts


@login_required
def djangoAllPosts(request):

    print("In DjangoAllPosts")

    user = request.user
    userLoggedIn = request.user.username
    # Get the user ID of the logged in user for the User object
    user_id = request.user.id
    userName = User.objects.get(id=user_id)
    print(userName)
    print(user)
    print(userLoggedIn)
    # TODO: most recent posts first, how to do?  Need to sort the below.

    # user = User.objects.values('username')

    # userName = User.objects.get(id=1)
    # test = userName.username
# this is a queryset of Posts objects only
    # postings = Posts.objects.all().order_by('-createdDate')
    postings = Posts.objects.filter().order_by('-createdDate')

    # Pagination details.
    postsPagination = postings
    # Show this many postings per page.
    paginator = Paginator(postsPagination, 10)

    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    # Get the likeList for the like icon
    likeList = returnlikeList(request)

    return render(request, "network/allPosts.html", {"page_obj": page_obj, "postings": postings, "likeList": likeList})


@login_required
def returnlikeList(request):
    # Just want to determine if the current user likes a particular post or not.
    user_id = request.user.id
    # This will return a queryset of all objects that the user likes.
    # likedUser = Posts.objects.filter(likedUser = user_id)

    # likedUser = Posts.objects.get(likedUser = user_id)
    likedUser = Posts.objects.filter(likedUser=user_id)

    print(likedUser)

    likeList = []

# This will create a list of all the posts that a user likes.
    for like in likedUser:
        # if (like.user.id == user_id):
        #     print("yes")
        currentObject = User.objects.get(id=user_id)
        # This is the ID of the user.  can throw this away.
        print(currentObject.id)
        # This is the post.id that the current user likes
        print(like.id)
        likeList.append(like.id)

    return likeList


@login_required
def getProfile(request, username):
    print("In getProfile")
    # Information for the logged in user.  Not really relevant for the most part.
    # if the logged in user is different then link clicked user, then display the folllow and  unfollow buttons.
    user_id = request.user.id
    user_name = request.user.username

    # Information of the user that we need to retrieve posts for.  This is the user that we need to check
    # if they are in the following list and then display the Follow  Unfollow buttons appropriately
    # on the profile.
    print(username)
    user = User.objects.get(username=username)
    print(user.id)
    profileUser = user.id
    # FIXME:
    try:
        isFollowing = getFollowingFlag(request, username)
    except:
        print("This user is following no one!")
        isFollowing = False

    # FIXME: Need to think about clicking on links and  on the title bar.  there is a difference.

    # All of the listings we need to display in the profile page.
    # Need to check for empty queryset.  Doesnotexist error.

    try:
        posts = Posts.objects.filter(creator=profileUser)
        postsUser = posts.order_by('-createdDate')

        # Pagination details.
        postsPagination = postsUser
        # Show this many postings per page.
        paginator = Paginator(postsPagination, 2)

        page_number = request.GET.get('page', '1')
        page_obj = paginator.get_page(page_number)

        noListings = False
    except Posts.DoesNotExist:
        print("blah")
        noListings = True

    # Need to pass a value if the user has no postings.

    # Returns querysets of User objects.

    try:
        follow = Follow.objects.get(followUser=profileUser)
        followObject = True
    except:
        Follow.DoesNotExist
        followObject = False

    # if follow.followers.all().count() != 0:
    #     countFollowers = follow.followers.all().count()

    if followObject != False:
        countFollowers = follow.followers.all().count()

    else:
        countFollowers = 0

    if followObject == True:

        # Do not use this at the moment.  May add in future./
        followers = follow.followers.all()

    if followObject == True:

        countFollowing = follow.following.all().count()
    else:
        countFollowing = 0

      # Do not use this at the moment.  May add in future.
    if followObject == True:
        following = follow.following.all()

    likeList = returnlikeList(request)

    if followObject == False:
        # This one does not return the users that are following and followers.  May or may not use that.
        return render(request, "network/profile.html", {"page_obj": page_obj, "noListings": noListings, "postings": postsUser, "countFollowers": countFollowers, "countFollowing": countFollowing, "isFollowing": isFollowing})
    else:
        return render(request, "network/profile.html", {"page_obj": page_obj, "noListings": noListings, "postings": postsUser, "countFollowers": countFollowers, "countFollowing": countFollowing, "username": username, "isFollowing": isFollowing, "likeList": likeList})


# The username here is the user that the logged in user wants to follow.
# This method does both following and unfollowing.
@login_required
def follow(request, username):
    print("in follow function")
    isFollowing = False
    # Current user that wants to add a follower.  this is the User object.
    userLoggedin = request.user
    IDOfUserLoggedIn = userLoggedin.id

    # test = User.objects.get(id=IDOfUserLoggedIn)

    print(userLoggedin)
    # This is the user that the logged in user wants to follow.

    # Need the ID of the user you want to add to your following list.
    print(username)
    un = username
    # user id of the user to be added to following list.
    userID = User.objects.get(username=un)
    userIDNewFollowing = userID.id

    # userIDTest = User.objects.get(username=userLoggedin)
    # IDTst = userIDTest.id

# FIXME:
    try:
        UserLoggedIn = Follow.objects.get(followUser=IDOfUserLoggedIn)
    except:
        # If they don't have a Folow object, need to create one.
        UserLoggedIn = Follow(followUser_id=IDOfUserLoggedIn)
        UserLoggedIn.save()

    # user id and username of the logged in user.
    user_id = request.user.id
    user_name = request.user.username

    try:
        # Follow object of the logged in user. You want the id of the followUser, not the id of the Follow object itself.
        follow = Follow.objects.get(followUser_id=user_id)
        # Some users that have not created a follower or following anyone will not have a Follow object instantiated and therefore
        # need to create one.
        followObject = True
    except Follow.DoesNotExist:
        print("This user has no folow objects!")
        # In this case we don't need to check for existing
        # followers and following but must create a Follow object.
        followObject = False

    if followObject == True:
        # returns a Qs of followers.  Right now I don't list the follwers by name, but could be an enhancement.
        followers = follow.followers.all()

    if followObject == True:

        # FIXME: returns a Qs of those theat the user follows. Need to test this to see if the new user is in this QS.  If it is not, then add it.
        following = follow.following.all()

        # FIXME: Needs to find the value in the list.
        # if userIDNewFollowing in following:
        if userID in following:

            # remove the user as a follower if they are already in the list. Set the flag for use in the template.
            follow.following.remove(userIDNewFollowing)
            follow.save()
            print(follow.following.all())
            isFollowing = False

        else:

            # add the user to to the following list if they are not already there.  Set the flag for use in the template.
            follow.following.add(userIDNewFollowing)

            follow.save()
            print(follow.following.all())
            isFollowing = True

    # TODO: Or should I display the Following list here?
    return HttpResponseRedirect(reverse("getFollowing"))

# The username here is the user that the logged in user wants to follow.
# This method does both following and unfollowing for the JavaScript version of the button.  Needs to return JSON.


@login_required
def followUser(request, username):
    # if follow from the JSON = false, then need to Unfollow the user.  Opposite if true.
    print("In followUser in Django!")

    # Need the ID of the user you want to add or remove from the following list.
    print(username)
    un = username
    # user id of the user to be added to following list.
    userID = User.objects.get(username=un)
    userIDNewFollowing = userID.id

    # user id and username of the logged in user.
    user_id = request.user.id
    user_name = request.user.username

    userLoggedin = request.user
    IDOfUserLoggedIn = userLoggedin.id

    print(userLoggedin)

    # FIXME: This is for cases where there is no Follow object.
    try:
        UserLoggedIn = Follow.objects.get(followUser=IDOfUserLoggedIn)
    except:
        # If they don't have a Folow object, need to create one.
        UserLoggedIn = Follow(followUser_id=IDOfUserLoggedIn)
        UserLoggedIn.save()

    follow = Follow.objects.get(followUser_id=user_id)

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if request.method == "PUT":

        data = json.loads(request.body)
        followBoolean = data.get("follow")
        print(followBoolean)
        if (followBoolean):
            # If true, then need to add the user to the following list of the logged in user.  request.user.username.
            # add the user to to the following list if they are not already there.  Set the flag for use in the template.
            follow.following.add(userIDNewFollowing)

            follow.save()
            print(follow.following.all())

            return JsonResponse({"data": data["follow"]}, safe=False)

        else:

            # follow = false, remove the user from the logged in users following list.
            # TODO: When you click Unfollow you end up here and return follow: false.

         # remove the user as a follower if they are already in the list. Set the flag for use in the template.
            follow.following.remove(userIDNewFollowing)
            follow.save()
            print(follow.following.all())

            return JsonResponse({"data": data["follow"]}, safe=False)


@login_required
def getFollowingFlag(request, username):
    print("In getFollowingFlag")

    isFollowing = False
    # Current user that wants to add a follower.  this is the User object.
    userLoggedin = request.user
    print(userLoggedin)
    # This is the user that the logged in user wants to follow.

    # Need the ID of the user you want to add to your following list.
    print(username)
    # user id of the user to be added to following list.
    userID = User.objects.get(username=username)
    userIDNewFollowing = userID.id
    UserLoggedIn = Follow.objects.get(followUser=userLoggedin)

    # user id and username of the logged in user.
    user_id = request.user.id
    user_name = request.user.username

    try:
        # Follow object of the logged in user.
        follow = Follow.objects.get(followUser_id=user_id)
        followObject = True
    except Follow.DoesNotExist:
        print("This user has no folow objects!")
        # In this case we don't need to check for existing
        # followers and following
        followObject = False

    if followObject == True:
        # returns a Qs of followers.
        followers = follow.followers.all()

# FIXME: This condition is not working.

    test = User.objects.get(username=username)

    if test == userLoggedin:
        isFollowing = None
        return isFollowing

    if followObject == True:

        # FIXME: returns a Qs of those theat the user follows. Need to test this to see if the new user is in this QS.  If it is not, then add it.
        following = follow.following.all()
        # test = Follow.objects.filter(followUser_id=user_id)

        # FIXME: Needs to find the value in the list.
        # if userIDNewFollowing in following:
        if userID in following:

            # remove the user as a follower.
            # follow.following.remove(userIDNewFollowing)
            isFollowing = True
            return isFollowing

        else:

            # add the user to to the following list.
            # follow.following.add(userIDNewFollowing)
            # isFollowing = False
            # TODO: Is this else actually used.
            return isFollowing
    else:
        isFollowing = False
        return isFollowing


@login_required
def getFollowing(request):
    print("In getFollowing")
    user = request.user
    print(user)

    # From the Follow object, get the "following" users and then retrieve all posts for those users with the most recent posts first.

    user_id = request.user.id
    user_name = request.user.username

    # If the user doesnlt have any followers, following or posts it will throw an error.
    try:
        currentOBJ = Follow.objects.get(followUser=user_id)
        displayNothing = False
        noFollowersForUser = False
    except Follow.DoesNotExist:
        print("This user follows no one!")
        displayNothing = True
        noFollowersForUser = True

    if displayNothing != True:

        following = currentOBJ.following.all()
        if following.count() == 0:
            noFollowersForUser = True

        # FIXME: if this amounts to zero, then need to set noFollowersForUser = True

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
                    # displayNothing = True

    if noFollowersForUser == True:
        return render(request, "network/following.html", {"displayNothing": displayNothing})

    else:
        # Sort by created date.
        if noFollowersForUser:
            return render(request, "network/following.html", {"displayNothing": displayNothing})

        else:

            PostsByDate = newQueryset.order_by('-createdDate')

            # Pagination details.
            postsPagination = PostsByDate
            # Show this many postings per page.
            paginator = Paginator(postsPagination, 7)

            page_number = request.GET.get('page', '1')
            page_obj = paginator.get_page(page_number)

            # Get the likeList for the like icon
            likeList = returnlikeList(request)

    return render(request, "network/following.html", {"page_obj": page_obj, "listings": PostsByDate, "UserObject": UserObject, "displayNothing": displayNothing, "likeList": likeList})


@login_required
def viewJSON(request):
    return render(request, "network/JSONAPI.html")

@login_required
def viewSwaggerDocs(request):
    return render(request, "swagger-ui.html")


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
