from django import forms
from .models import User, Posts, Comment, Following, UserProfile


class CreateNewPost(forms.ModelForm):
    post_content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "create-new-post",
                # "autofocus": True,
                "rows": "4",
                "placeholder": "Let the world know what you think you're doing",
            }
        ),
    )

    class Meta:
        model = Posts
        fields = ["post_content"]


class CreateComment(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "add-comment",
                "rows": "4",
                "placeholder": "Say something on this post",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["content"]
