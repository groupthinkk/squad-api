import random

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from rest_framework import status, generics
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Turker, HIT, InstagramPrediction, TurkerPerformance
from .serializers import (
    TurkerSerializer, HITSerializer, InstagramPredictionSerializer,
    TurkerPerformanceSerializer,
)


API_KEYS = (
    'CazMCDN5G2SuFhET3BuXdLIW01PQxisNLwKRIw',
)


def bad_request(message):
    return Response({
        'status': 'error',
        'messages': message,
    }, status=status.HTTP_400_BAD_REQUEST)


class APIKeyPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_superuser or
            request.GET.get('api_key') in API_KEYS or
            request.POST.get('api_key') in API_KEYS
        )


class TurkerList(generics.ListCreateAPIView):

    queryset = Turker.objects.all()
    serializer_class = TurkerSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['turker_id']


class TurkerPerformanceList(generics.ListAPIView):

    queryset = TurkerPerformance.objects.all().order_by('-correctness')
    serializer_class = TurkerPerformanceSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]


class HITList(generics.ListCreateAPIView):

    queryset = HIT.objects.select_related()
    serializer_class = HITSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['hit_id', 'turker', 'status']

    def post(self, request, format=None):
        hit = HIT()
        hit.hit_id = request.data.get('hit_id')
        hit.turker = get_object_or_404(
            Turker,
            turker_id=request.data.get('turker_id'),
        )
        hit.status = request.data.get('status') or ''

        queue_queryset = HIT.instagram_queue.get_queryset()

        if 'queue_id' in request.data:
            queue_id = request.data['queue_id']
            try:
                queue = queue_queryset.get(id=int(queue_id))
            except ValueError:
                return bad_request('Invalid queue_id.')
            except queue_queryset.model.DoesNotExist:
                return bad_request(
                    'Queue with queue_id={} does not exist.'.format(queue_id)
                )
        else:
            queue_ids = [h.instagram_queue_id for h in hit.turker.hit_set.all()]
            queues = queue_queryset.exclude(id__in=queue_ids)
            try:
                queue = queues.all()[random.randint(0, queues.count() - 1)]
            except ValueError:
                message = 'No more queues available for turker_id: {}.'.format(
                    request.data.get('turker_id'),
                )
                return bad_request(message)

        hit.instagram_queue = queue

        try:
            hit.full_clean()
        except ValidationError as ve:
            return bad_request(ve.messages)

        hit.save()

        serializer = HITSerializer(hit)

        return Response(serializer.data)


class InstagramPredictionList(generics.ListCreateAPIView):

    queryset = InstagramPrediction.objects.select_related()
    serializer_class = InstagramPredictionSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['hit']

    def post(self, request, format=None):
        prediction = InstagramPrediction()
        prediction.hit = get_object_or_404(
            HIT,
            pk=request.data.get('hit_id'),
        )
        prediction.comparison = get_object_or_404(
            InstagramPrediction.comparison.get_queryset(),
            pk=int(request.data.get('comparison_id')),
        )
        prediction.choice_id = int(request.data.get('choice_id'))
        prediction.ux_id = request.data.get('ux_id') or ''
        prediction.decision_milliseconds = request.data.get('decision_milliseconds')

        post_a = prediction.comparison.post_a
        post_b = prediction.comparison.post_b

        if prediction.choice_id == post_a.id:
            prediction.correct = post_a.likes_count > post_b.likes_count
        else:
            prediction.correct = post_b.likes_count > post_a.likes_count

        try:
            prediction.full_clean()
        except ValidationError as ve:
            return bad_request(ve.messages)

        prediction.save()

        serializer = InstagramPredictionSerializer(prediction)

        return Response(serializer.data)
