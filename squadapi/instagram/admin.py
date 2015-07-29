from django.contrib import admin

from .models import User, Post, Normalization


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Normalization)
