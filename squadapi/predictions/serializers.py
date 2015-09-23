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
            'correct',
            'decision_milliseconds',
            'ux_id',
            'created_datetime',
        )
        depth = 1
