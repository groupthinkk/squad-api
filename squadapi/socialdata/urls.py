from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import InstagramUserList, InstagramPostList

urlpatterns = [
    url(r'^instagram/users/$', InstagramUserList.as_view()),
    url(r'^instagram/posts/$', InstagramPostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
