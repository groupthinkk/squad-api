from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Turker, InstagramPrediction
from .serializers import TurkerSerializer, InstagramPredictionSerializer


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


class TurkerList(generics.ListCreateAPIView):

    queryset = Turker.objects.all()
    serializer_class = TurkerSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]
    filter_fields = ['turker_id']

    def perform_create(self, serializer):
        queue = Turker.instagram_queue.get_queryset().first()
        serializer.save(instagram_queue=queue)


class InstagramPredictionList(generics.ListCreateAPIView):

    queryset = InstagramPrediction.objects.all()
    serializer_class = InstagramPredictionSerializer
    paginate_by = 25
    permission_classes = [APIKeyPermission]

    def post(self, request, format=None):
        turker = get_object_or_404(
            Turker,
            turker_id=request.POST.get('turker_id'),
        )

        prediction = InstagramPrediction()
        prediction.turker = turker
        prediction.comparison = get_object_or_404(
            InstagramPrediction.comparison.get_queryset(),
            queue=turker.instagram_queue,
            comparison_id=int(request.POST.get('comparison_id')),
        )
        prediction.choice_id = int(request.POST.get('choice_id'))
        prediction.decision_milliseconds = request.POST.get('decision_milliseconds')

        try:
            prediction.full_clean()
        except ValidationError as ve:
            return Response({
                'status': 'error',
                'messages': ve.messages,
            }, status=status.HTTP_400_BAD_REQUEST)

        prediction.save()

        serializer = InstagramPredictionSerializer(prediction)

        return Response(serializer.data)
