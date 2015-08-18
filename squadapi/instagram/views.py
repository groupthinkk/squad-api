import json
import random

from collections import OrderedDict
from datetime import datetime, timedelta

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
        if 'username' in request.GET:
            try:
                user = User.objects.get(username=request.GET['username'])
            except User.DoesNotExist:
                return Response()
        else:
            users = User.objects
            user = users.all()[random.randint(0, users.count() - 1)]

        exclude = []

        if 'exclude' in request.GET:
            exclude = request.GET['exclude'].split(',')

        posts = Post.objects.filter(user=user).exclude(post_id__in=exclude)

        post0 = posts.all()[random.randint(0, posts.count() - 1)]

        since = post0.created_datetime - timedelta(weeks=1)
        until = post0.created_datetime + timedelta(weeks=1)

        for post1 in posts.filter(
            created_datetime__lt=until,
            created_datetime__gte=since,
        ).exclude(post_id=post0.post_id):
            l0 = post0.likes_count
            l1 = post1.likes_count

            if 5 <= abs((l0 - l1) / l0 * 100) < 50:
                break

        return Response(OrderedDict([
            ('id', post0.post_id),
            ('posts', [map(_format_post, [post0, post1])]),
        ]))
