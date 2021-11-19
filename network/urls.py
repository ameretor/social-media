from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post-comment/<str:action>", views.post_comment_view, name="post-comment"),
    path("load_comments/<int:post_id>", views.load_comments, name="load_comments"),
    path("user_profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
