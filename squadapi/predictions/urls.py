from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import TurkerList, InstagramPredictionList

urlpatterns = [
    url(r'^predictions/turkers/$', TurkerList.as_view()),
    url(r'^predictions/instagram/$', InstagramPredictionList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
