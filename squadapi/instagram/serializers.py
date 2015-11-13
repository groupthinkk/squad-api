from rest_framework import serializers

from .models import User, Post, PostComparison, PostComparisonQueue


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'username',
            'followers',
            'image_url',
        )
        depth = 1


class PostSerializer(serializers.ModelSerializer):

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
        depth = 1


class PostComparisonSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComparison
        fields = (
            'id',
            'user',
            'post_a',
            'post_b',
        )
        depth = 1


class PostComparisonQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComparisonQueue
        fields = (
            'id',
            'name',
            'comparisons',
        )
        depth = 0
