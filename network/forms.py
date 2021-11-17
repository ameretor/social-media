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


class EditProfileForm(forms.ModelForm):
    """
    Form to create new profile
    * name
    * date_of_birth
    * about
    * profile_picture
    """

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "id": "date-of-birth",
                "type": "date",
                "placeholder": "Date of birth",
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = ["name", "date_of_birth", "about", "profile_picture"]
        labels = {
            "name": "Name",
            "date_of_birth": "Date of birth",
            "about": "About",
            "profile_picture": "Profile picture",
        }
        widgets = {
            "name": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "name",
                    "type": "text",
                    "placeholder": "Name",
                }
            ),
            "about": widgets.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "about",
                    "rows": "4",
                    "placeholder": "About",
                }
            ),
            "date_of_birth": widgets.DateInput(
                attrs={
                    "class": "form-control",
                    "id": "date-of-birth",
                    "type": "date",
                    "placeholder": "Date of birth",
                }
            ),
            "profile_picture": widgets.FileInput(
                attrs={
                    "class": "form-control",
                    "id": "profile-picture",
                    "type": "file",
                    "placeholder": "Profile picture",
                }
            ),
        }
