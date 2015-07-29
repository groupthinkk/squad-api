from django.db import models


class User(models.Model):

    user_id = models.CharField(max_length=64, unique=True)
    username = models.CharField(max_length=64)


class Post(models.Model):

    user = models.ForeignKey(User)
    post_id = models.CharField(max_length=64, unique=True)
    caption = models.TextField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(db_index=True)


class Normalization(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    data = models.TextField()
