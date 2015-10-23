import json
import random

from collections import OrderedDict
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from .models import User, Post, PostComparison, PostComparisonQueue
from .serializers import (
    UserSerializer, PostSerializer, PostComparisonSerializer,
    PostComparisonQueueSerializer,
)


API_KEYS = (
    'CazMCDN5G2SuFhET3BuXdLIW01PQxisNLwKRIw',
)


class APIKeyPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_superuser or
            request.GET.get('api_key') in API_KEYS or
            request.POST.get('api_key') in API_KEYS
        )


def bad_request(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['user_id', 'username']


class PostList(generics.ListAPIView):

    queryset = Post.objects.all().order_by('-created_datetime')
    serializer_class = PostSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]

    def get_queryset(self):
        if 'username' in self.request.query_params:
            return self.queryset.filter(
                user__username=self.request.query_params['username'],
            )
        return self.queryset


class PostComparisonList(generics.ListCreateAPIView):

    queryset = PostComparison.objects.select_related('user', 'post_a', 'post_b')
    serializer_class = PostComparisonSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['id']


class PostComparisonQueueList(generics.ListCreateAPIView):

    queryset = PostComparisonQueue.objects.all()
    serializer_class = PostComparisonQueueSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['id']

    def post(self, request, format=None):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'))
        except User.DoesNotExist:
            return bad_request(
                'Required parameter missing or does not exist: user_id'
            )

        post_id = request.data.get('post_id') or ''

        if not post_id:
            return bad_request('Required parameter missing: post_id')

        queue = PostComparisonQueue(
            name='auto-{}'.format(post_id),
        )
        queue.save()

        serializer = PostComparisonQueueSerializer(queue)

        return Response(serializer.data)


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

    permission_classes = [APIKeyPermission]

    def get_random_post(self, username=None, exclude=[]):
        if username is not None:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response()
        else:
            users = User.objects
            user = users.all()[random.randint(0, users.count() - 1)]

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

    def get(self, request, format=None):
        username = None
        if 'username' in request.GET:
            username=request.GET['username']

        exclude = []

        if 'exclude' in request.GET:
            exclude = request.GET['exclude'].split(',')

        return self.get_random_post(username, exclude)

    def post(self, request, format=None):
        username = None
        if 'username' in request.POST:
            username = request.POST['username']

        exclude = []
        if 'exclude' in request.POST:
            exclude = request.POST['exclude'].split(',')

        return self.get_random_post(username, exclude)
