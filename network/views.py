from django.core import serializers
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Comment, Following, UserProfile

# Adding forms
from .forms import CreateNewPost


def index(request):
    all_posts = Posts.objects.all()
    data = serialize("json", all_posts)

    return render(
        request,
        "network/index.html",
        {"create_post_form": CreateNewPost, "data": data},
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

    if request.method == "POST" and action == "post":
        form = CreateNewPost(request.POST)

        if form.is_valid():
            content = form.cleaned_data["post_content"]
            print("Form is valid in post action")

            posts = Posts(user=User.objects.get(pk=request.user.id), content=content)
            posts.save()
            all_posts = Posts.objects.all()
            data = serialize("json", all_posts)
        # return HttpResponse(data, content_type="json")
        # return HttpResponseRedirect(reverse("index"))
        return JsonResponse({"message": "Posted successfully."}, safe=False)
        # return render(
        #     request, "network/index.html", {"create_post_form": form, "data": data}
        # )


@login_required(login_url="/login")
def load_posts(request, action):

    all_posts = Posts.objects.all()
    return JsonResponse([post.serialize() for post in all_posts], safe=False)
