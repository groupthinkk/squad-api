from rest_framework import serializers

from .models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ('caption', 'created_datetime', 'likes_count', 'comments_count')
