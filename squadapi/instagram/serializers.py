from rest_framework import serializers

from .models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'username', 'followers')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            'user',
            'caption',
            'image_url',
            'likes_count',
            'comments_count',
            'created_datetime',
        )
