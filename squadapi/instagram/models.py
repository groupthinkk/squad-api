from django.db import models


class User(models.Model):

    user_id = models.CharField(max_length=64, default='', blank=True)
    username = models.CharField(max_length=64, unique=True)
    followers = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):

    user = models.ForeignKey(User)
    post_id = models.CharField(max_length=64, unique=True)
    caption = models.TextField()
    image_url = models.URLField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(db_index=True)

    def image_tag(self):
        return '<img src="{0}" width="50"/>'.format(self.image_url)
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'


class Normalization(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    data = models.TextField()
