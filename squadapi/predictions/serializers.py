from rest_framework import serializers

from .models import Turker, HIT, InstagramPrediction


class TurkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turker
        fields = ('id', 'turker_id')
        depth = 1


class HITSerializer(serializers.ModelSerializer):

    class Meta:
        model = HIT
        fields = (
            'id',
            'hit_id',
            'turker',
            'status',
            'instagram_queue',
            'created_datetime',
        )
        depth = 1


class InstagramPredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramPrediction
        fields = (
            'hit',
            'comparison',
            'choice',
            'correct',
            'decision_milliseconds',
            'ux_id',
            'created_datetime',
        )
        depth = 1
