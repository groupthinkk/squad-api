from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    TurkerList, HITList, InstagramPredictionList, TurkerPerformanceList,
    InstagramPostList,
)

urlpatterns = [
    url(r'^predictions/turkers/$', TurkerList.as_view()),
    url(r'^predictions/turkers/performance$', TurkerPerformanceList.as_view()),
    url(r'^predictions/hits/$', HITList.as_view()),
    url(r'^predictions/instagram/$', InstagramPredictionList.as_view()),
    url(r'^predictions/instagram/posts/$', InstagramPostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
