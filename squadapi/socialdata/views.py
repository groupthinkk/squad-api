from django.shortcuts import render

from rest_framework import generics

from .models import InstagramUser, InstagramPost
from .serializers import InstagramUserSerializer, InstagramPostSerializer


class InstagramUserList(generics.ListAPIView):

    queryset = InstagramUser.objects.all()
    serializer_class = InstagramUserSerializer
    paginate_by = 25


class InstagramPostList(generics.ListAPIView):

    queryset = InstagramPost.objects.all()
    serializer_class = InstagramPostSerializer
    paginate_by = 25
