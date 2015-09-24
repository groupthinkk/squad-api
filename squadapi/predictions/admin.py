from django.contrib import admin

from .models import Turker, HIT, InstagramPrediction


class TurkerAdmin(admin.ModelAdmin):

    list_display = [
        'turker_id',
        'updated_datetime',
        'created_datetime',
    ]

admin.site.register(Turker, TurkerAdmin)


class HITAdmin(admin.ModelAdmin):

    list_display = [
        'hit_id',
        'turker',
        'instagram_queue',
        'created_datetime',
    ]

admin.site.register(HIT, HITAdmin)


class InstagramPredictionAdmin(admin.ModelAdmin):

    list_display = [
        'hit',
        'comparison',
        'choice',
        'decision_milliseconds',
        'correct',
        'ux_id',
        'created_datetime',
    ]

admin.site.register(InstagramPrediction, InstagramPredictionAdmin)
