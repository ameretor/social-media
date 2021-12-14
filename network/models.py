from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    """
    * User Data adding additional fields.
    """

    user = models.OneToOneField(User, on_delete=CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        User, related_name="followers", default=None, blank=True
    )
    image = models.ImageField(
        default="images/default.png", upload_to="images/", blank=True, null=True
    )

    # Resize image to 300x300
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def serialize(self):
        return {
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "about": self.about,
            "image": self.image,
        }

    def __str__(self):
        return f"Id: {self.id} User: {self.user.username} DOB: {self.date_of_birth}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile created 2")
    else:
        print("User Profile not created 2")


class Posts(models.Model):
    """
    * Storing collection of posts.
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_posts")
    content = models.TextField(blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, default=None, blank=True, related_name="liked_posts"
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def serialize(self):
        return {
            "content": self.content,
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

    def serialize(self):
        return {
            "user": self.user.username,
            "post": self.post.content,
            "comment_content": self.comment_content,
            "date_of_comment": self.date_of_comment,
        }

    def __str__(self):
        return f"user {self.user} commented (comment id: {self.id}) {self.comment_content} on {self.post.content} on {self.date_of_comment}"


class Following(models.Model):
    """
    * Collection of posts made by followed users
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="following_user")
    user_following = models.ForeignKey(User, on_delete=CASCADE, related_name="follower")
    followed = models.BooleanField(default=False)

    def __str__(self):
        return f"Follow id {self.id} represents {self.user} is following {self.user_following}"

    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Followings"
        unique_together = ("user", "user_following")

    def get_user_followed_posts(self):
        return self.user_following.user_posts.order_by("-time_stamp").all()


class Likes(models.Model):
    """
    * Collection of posts liked by users
    """

    user = models.ForeignKey(User, on_delete=CASCADE, related_name="likes_user")
    post = models.ForeignKey(Posts, on_delete=CASCADE, related_name="likes_post")
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked post {self.post.id}"
