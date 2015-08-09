import json
import random

from collections import OrderedDict
from datetime import datetime

from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Post, Normalization
from .serializers import UserSerializer, PostSerializer


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginate_by = 25


class PostList(generics.ListAPIView):

    queryset = Post.objects.all().order_by('-created_datetime')
    serializer_class = PostSerializer
    paginate_by = 25

    def get_queryset(self):
        if 'username' in self.request.query_params:
            return self.queryset.filter(
                user__username=self.request.query_params['username'],
            )
        return self.queryset


def _format_post(post):
    return OrderedDict([
        ('username', post.user.username),
        ('caption', post.caption),
        ('image_url', post.image_url),
        ('likes_count', post.likes_count),
        ('comments_count', post.comments_count),
        ('created_datetime', post.created_datetime),
    ])


class PostRandom(APIView):

    def get(self, request, format=None):
        queryset = Normalization.objects

        if 'username' in request.GET:
            print(request.GET)
            queryset = queryset.filter(user__username=request.GET['username'])

        try:
            normalization = queryset.order_by('?').first()
        except Normalization.DoesNotExist:
            return Response()

        user = normalization.user
        data = json.loads(normalization.data)
        year = random.choice(list(data.keys()))

        posts = Post.objects.filter(
            user=user,
            created_datetime__year=int(year),
        ).order_by('?')

        exclude = []

        if 'exclude' in request.GET:
            exclude = request.GET['exclude'].split(',')

        post_0 = posts.exclude(post_id__in=exclude).first()

        threshold = data[year]['stdev'] / 2

        for post in posts.exclude(post_id=post_0.id):
            if not post_0:
                post_0 = post
                continue

            if abs(post_0.likes_count - post.likes_count) > threshold:
                post_1 = post
                break

        return Response(OrderedDict([
            ('id', post_0.post_id),
            ('posts', [map(_format_post, [post_0, post_1])]),
            ('normalization', OrderedDict(sorted(data.items(), key=lambda t: t[0]))),
        ]))
