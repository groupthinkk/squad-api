from rest_framework import serializers

from .models import (
    Turker, HIT, InstagramPrediction, TurkerPerformance, InstagramPost,
)


class TurkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turker
        fields = ('id', 'turker_id')
        depth = 1


class TurkerPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TurkerPerformance
        fields = ('turker', 'correctness', 'updated_datetime')
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

    contains_target = serializers.ReadOnlyField()

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
            'contains_target',
        )
        depth = 1


class InstagramPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramPost
        fields = (
            'id',
            'post',
            'hit_id',
            'lower_bound',
            'upper_bound',
            'updated_datetime',
            'created_datetime',
        )
        depth = 1
