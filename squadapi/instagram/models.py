from django.db import models


class User(models.Model):

    username = models.CharField(max_length=64)


class Post(models.Model):

    user = models.ForeignKey(User)
    caption = models.TextField()
    likes_count = models.IntegerField()
    comments_count = models.IntegerField()
    created_datetime = models.DateTimeField(db_index=True)


class Normalization(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    data = models.TextField()
