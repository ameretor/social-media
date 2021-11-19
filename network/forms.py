from django import forms
from django.forms import widgets
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


class DateInput(forms.DateInput):
    input_type = "date"


class EditProfileForm(forms.ModelForm):
    # Containing fields name, date_of_birth, about, profile_picture
    name = forms.CharField(
        label="Name:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Name",
            }
        ),
    )

    about = forms.CharField(
        label="Bio:",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "about",
                "rows": "4",
                "placeholder": "About",
            }
        ),
    )

    profile_picture = forms.ImageField(
        label="Profile Pic:",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "id": "profile_picture",
                "placeholder": "Profile Picture",
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = ["name", "date_of_birth", "about", "profile_picture"]
        widgets = {"date_of_birth": DateInput()}
