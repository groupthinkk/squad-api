from rest_framework import serializers

from .models import Turker, InstagramPrediction


class TurkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turker
        fields = ('id', 'turker_id', 'instagram_queue')
        depth = 1


class InstagramPredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramPrediction
        fields = (
            'turker',
            'comparison',
            'choice',
            'decision_milliseconds',
            'created_datetime',
        )
        depth = 1
