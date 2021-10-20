from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    """
    * User Data adding additional fields.
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="images", blank=True, null=True)

    def serialize(self):
        return {
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "about": self.about,
            "profile_picture": self.profile_picture,
        }

    def __str__(self):
        return f"Id: {self.id} User: {self.user.username} DOB: {self.date_of_birth}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile created")
    else:
        print("User Profile not created")


class Posts(models.Model):
    """
    * Storing collection of posts.
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_posts")
    content = models.TextField(blank=True)
    reply = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "content": self.content,
            "reply": self.reply,
            "time_stamp": self.time_stamp,
        }

    def __str__(self):
        return f"Post Id: {self.id} User: {self.user} posted: {self.content}"


class Comment(models.Model):
    """
    * Comments made information
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="comments_user")
    post = models.ForeignKey(Posts, on_delete=CASCADE, related_name="comments_post")
    comment_content = models.TextField(blank=True)
    date_of_comment = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="commented on"
    )

    def __str__(self):
        return f"user {self.user} commented (comment id: {self.id}) {self.comment_content} on {self.post.content} on {self.date_of_comment}"


class Following(models.Model):
    """
    * Collection of posts made by followed users
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="following_user")
    user_follower = models.ForeignKey(User, on_delete=CASCADE, related_name="follower")
    post = models.ForeignKey(Posts, on_delete=CASCADE, related_name="following_post")

    def __str__(self):
        return f"{self.user_follower} is following {self.user} on post {self.post.id}"
