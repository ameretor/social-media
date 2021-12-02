from django.contrib import admin
from .models import User, UserProfile, Posts, Comment, Following, Likes

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Likes)