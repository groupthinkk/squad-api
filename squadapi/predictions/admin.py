from django.contrib import admin

from .models import Turker, InstagramPrediction


class TurkerAdmin(admin.ModelAdmin):

    list_display = [
        'turker_id',
        'instagram_queue',
        'updated_datetime',
        'created_datetime',
    ]

admin.site.register(Turker, TurkerAdmin)


class InstagramPredictionAdmin(admin.ModelAdmin):

    list_display = [
        'turker',
        'comparison',
        'choice',
        'decision_milliseconds',
        'correct',
        'ux_id',
        'created_datetime',
    ]

admin.site.register(InstagramPrediction, InstagramPredictionAdmin)
