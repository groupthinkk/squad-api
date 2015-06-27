from django.db import models


class InstagramUser(models.Model):

    username = models.CharField(max_length=64)


class InstagramPost(models.Model):

    user = models.ForeignKey(InstagramUser)
    caption = models.TextField()
    likes_count = models.IntegerField()
    comments_count = models.IntegerField()
    created_datetime = models.DateTimeField(db_index=True)
