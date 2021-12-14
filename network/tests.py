import os
import pathlib
import unittest

# django
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase, Client
from django.contrib import auth
from django.db import transaction, IntegrityError

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from .models import *
import time

# Create your tests here.


def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# driver = webdriver.Chrome(ChromeDriverManager().install())

# print(driver.get(file_uri("./network/templates/network/index.html")))


# class test_title(LiveServerTestCase):
#     # test Home page title
#     def test_title(self):
#         self.driver = webdriver.Chrome(ChromeDriverManager().install())
#         self.driver.get(self.live_server_url)
#         time.sleep(3)
#         print(self.live_server_url)

#     def tearDown(self):
#         self.driver.quit()

#         self.assertEqual(self.driver.title, "Ocean 4")


# test login page
class test_login(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=self.options
        )
        self.driver.get(self.live_server_url + "/login")

    def test_login(self):
        self.driver.find_element_by_name("username").send_keys("test")
        self.driver.find_element_by_name("password").send_keys("test")
        self.driver.find_element_by_name("login_btn").click()

    def tearDown(self):
        self.driver.quit()


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="test")
        self.post = Posts.objects.create(user=self.user, content="test")
        self.comment = Comment.objects.create(
            user=self.user, comment_content="test", post=self.post
        )

    def test_posts(self):
        self.assertEqual(Posts.objects.all().count(), 1)

    #    test UserProfile is autocreated
    def test_user_profile(self):
        self.assertEqual(UserProfile.objects.all().count(), 1)

    # test image path
    def test_default_image(self):
        image_path = UserProfile.objects.get(user=self.user).image.path[73:]
        self.assertEqual(image_path, "default.png")

    # test comments
    def test_comments(self):
        self.assertEqual(Comment.objects.all().count(), 1)


# Views test cases
class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.posts = Posts.objects.create(user=self.user, content="test")
        self.comments = Comment.objects.create(
            user=self.user, post=self.posts, comment_content="test"
        )
        self.client = Client()

    # test index page
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    # test login page
    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    # test register redirect
    def test_register_redirect(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 302)

    # test register page
    def test_register(self):
        self.c = Client()
        try:
            with transaction.atomic():
                self.c_registered = auth.get_user(self.c)
                new_user = User.objects.all().count()
        except IntegrityError:
            pass
        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "email": "test@example.com",
                "password": "test",
                "confirmation": "test",
            },
        )

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.url, "/login")
        # self.assertTrue(self.c_registered.is_authenticated)
        self.assertEqual(new_user, 1)

    # test login redirect
    def test_login_redirect(self):
        response = self.client.post(
            reverse("login"), {"username": "test", "password": "test"}
        )
        c_logged_in = auth.get_user(self.client)
        self.assertEqual(response.status_code, 302)

    # test paginator index page
    def test_index_paginator(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["pag_obj"].paginator.num_pages, 1)

    def test_2_pages_paginator(self):
        for _ in range(6):
            Posts.objects.create(user=self.user, content="test")
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pag_obj"].paginator.num_pages, 2)

    # test post comment views
    def test_post_redirect(self):
        self.client.login(username="test", password="test")
        response = self.client.post("/post-comment/post", {"content": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    # test post comment create post comments
    def test_post_comment_create(self):
        self.client.login(username="test", password="test")
        post = Posts.objects.create(user=self.user, content="test")
        response = self.client.post(
            "/post-comment/post", {"content": "created post", "postID": post.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Posts.objects.all().count(), 2)
