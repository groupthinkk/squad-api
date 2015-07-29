from rest_framework import serializers

from .models import InstagramUser, InstagramPost


class InstagramUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = InstagramUser
        fields = ('id', 'username')


class InstagramPostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = InstagramPost
        fields = ('caption', 'created_datetime', 'likes_count', 'comments_count')
