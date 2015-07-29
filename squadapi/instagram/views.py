import json

from collections import OrderedDict
from datetime import datetime

from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InstagramUser, InstagramPost, InstagramData
from .serializers import InstagramUserSerializer, InstagramPostSerializer


class InstagramUserList(generics.ListAPIView):

    queryset = InstagramUser.objects.all()
    serializer_class = InstagramUserSerializer
    paginate_by = 25


class InstagramPostList(generics.ListAPIView):

    queryset = InstagramPost.objects.all()
    serializer_class = InstagramPostSerializer
    paginate_by = 25


class InstagramPostRandom(APIView):

    def get(self, request, format=None):
        user = InstagramUser.objects.order_by('?').first()
        post = InstagramPost.objects.filter(
            user=user,
            created_datetime__gt=datetime(2014, 1, 1),
        ).order_by('?').first()
        data = json.loads(InstagramData.objects.get(user=user).data)

        post_bucket = '{:02d}-{:02d}'.format(
            post.created_datetime.weekday(),
            post.created_datetime.hour,
        )

        bucket = data['buckets'][post_bucket]

        stdev_away = (post.likes_count - bucket['average']) / bucket['stdev']

        estimates = {}
        for k, v in data['buckets'].items():
            estimates[k] = max(int(v['average'] + v['stdev'] * stdev_away), 0)

        return Response(OrderedDict([
            ('username', user.username),
            ('caption', post.caption),
            ('created_datetime', post.created_datetime),
            ('likes_count', post.likes_count),
            ('comments_count', post.comments_count),
            ('estimates', OrderedDict(sorted(estimates.items(), key=lambda t: t[0]))),
        ]))
