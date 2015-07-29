from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserList, PostList, PostRandom

urlpatterns = [
    url(r'^instagram/users/$', UserList.as_view()),
    url(r'^instagram/posts/$', PostList.as_view()),
    url(r'^instagram/posts/random$', PostRandom.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
