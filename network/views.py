from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Comment, Following, UserProfile, Likes

# Adding forms
from .forms import CreateNewPost, CreateComment, EditProfileForm


def index(request):
    all_posts = Posts.objects.all().order_by("-time_stamp")
    data = serialize("json", all_posts)
    comments = Comment.objects.all()
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    pag_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/index.html",
        {
            "create_post_form": CreateNewPost,
            "data": data,
            "add_comment_form": CreateComment,
            "all_posts": all_posts,
            "comments": comments,
            "pag_obj": pag_obj,
            "paginator": paginator,
        },
    )


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="/login")
def post_comment_view(request, action):
    if request.method == "GET":
        return JsonResponse({"errors": "POST request required."})

    if request.method == "POST":
        if action == "post":
            form = CreateNewPost(request.POST)

            if form.is_valid():
                content = form.cleaned_data["post_content"]
                print("Form is valid in post action")

                posts = Posts(
                    user=User.objects.get(pk=request.user.id), content=content
                )
                posts.save()
                all_posts = Posts.objects.all()
                data = serialize("json", all_posts)
                # return JsonResponse({"message": "Posted successfully."}, safe=False)
                return HttpResponseRedirect(reverse("index"))

        # check if action is comments
        if action == "comments":
            form = CreateComment(request.POST)

            if form.is_valid():
                print("Comment form is valid")
                comment_content = form.cleaned_data["content"]

                try:
                    # get posts id from Posts models
                    this_post = Posts.objects.get(pk=request.POST["post-id"])
                    print(this_post)
                except Posts.DoesNotExist:
                    return JsonResponse({"errors": "Post does not exist."})

                comment = Comment(
                    user=User.objects.get(pk=request.user.id),
                    post=this_post,
                    comment_content=comment_content,
                )
                comment.save()

        return HttpResponseRedirect(reverse("index"))


def load_comments(request, post_id):

    all_comments = Comment.objects.all().order_by("-date_of_comment")
    users = UserProfile.objects.all()
    return JsonResponse([comment.serialize() for comment in all_comments], safe=False)


@login_required(login_url="/login")
def user_profile(request, user_id):
    # Get User Profile
    user_profile = UserProfile.objects.get(user=user_id)
    all_posts_by_user = Posts.objects.filter(user=user_id).order_by("-time_stamp")
    paginator = Paginator(all_posts_by_user, 2)
    page_number = request.GET.get("page")
    pag_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/user_profile.html",
        {
            "current_user": user_profile,
            "pag_obj": pag_obj,
            "all_posts_by_user": all_posts_by_user,
            "add_comment_form": CreateComment,
        },
    )


@login_required(login_url="/login")
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            user_profile = UserProfile.objects.get(user=request.user.id)
            user_profile.about = form.cleaned_data["about"]
            user_profile.name = form.cleaned_data["name"]
            fname = User.objects.get(pk=request.user.id)
            fname.first_name = user_profile.name
            fname.save()
            user_profile.date_of_birth = form.cleaned_data["date_of_birth"]
            user_profile.image = form.cleaned_data["profile_picture"]
            user_profile.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
    print("Request Get")
    return render(request, "network/edit_profile.html", {"form": EditProfileForm()})


@login_required(login_url="/login")
def likes_view(request):
    # if request.method == "GET":
    #     return JsonResponse({"errors": "POST request required."})

    # if request.method == "POST":
    #     if request.POST["action"] == "like":
    #         print(action)
    #         try:
    #             this_post = Posts.objects.get(pk=request.POST["post-id"])
    #             print(this_post)
    #         except Posts.DoesNotExist:
    #             return JsonResponse({"errors": "Post does not exist."})

    #         try:
    #             this_user = User.objects.get(pk=request.user.id)
    #             print(this_user)
    #         except User.DoesNotExist:
    #             return JsonResponse({"errors": "User does not exist."})

    #         like = Likes(user=this_user, post=this_post, liked=True)
    #         like.save()
    #         return JsonResponse({"message": "Liked successfully."}, safe=False)

    #     if request.POST["action"] == "unlike":
    #         print("Unlike action")
    #         try:
    #             this_post = Posts.objects.get(pk=request.POST["post-id"])
    #             print(this_post)
    #         except Posts.DoesNotExist:
    #             return JsonResponse({"errors": "Post does not exist."})

    #         try:
    #             this_user = User.objects.get(pk=request.user.id)
    #             print(this_user)
    #         except User.DoesNotExist:
    #             return JsonResponse({"errors": "User does not exist."})

    #         like = Likes.objects.get(user=this_user, post=this_post)
    #         like.delete()
    #         return JsonResponse({"message": "Unliked successfully."}, safe=False)
    user = request.user
    if request.method == "POST":
        post_id = request.POST["post-id"]
        post_obj = Posts.objects.get(pk=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Likes.objects.get_or_create(user=user, post=post_obj)

        if not created:
            if like.liked == True:
                like.liked = False
            else:
                like.liked = True

        like.save()
    return redirect("index")
