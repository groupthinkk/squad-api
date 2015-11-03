from django.contrib import admin

from .models import Turker, HIT, InstagramPrediction, TurkerPerformance
from .tasks import update_turker_performance


def _task_message(n):
    return '{0} task{1} successfully spawned.'.format(n, '' if n == 1 else 's')


class TurkerAdmin(admin.ModelAdmin):

    actions = [
        'update_turker_data',
    ]
    list_display = [
        'turker_id',
        'updated_datetime',
        'created_datetime',
    ]

    def update_turker_data(self, request, queryset):
        tasks = []
        for turker in queryset:
            tasks.append(update_turker_performance.delay(turker))
        ntasks = len([t for t in tasks if t])
        self.message_user(request, _task_message(ntasks))

admin.site.register(Turker, TurkerAdmin)


class TurkerPerformanceAdmin(admin.ModelAdmin):

    list_display = [
        'turker',
        'correctness',
        'updated_datetime',
    ]

admin.site.register(TurkerPerformance, TurkerPerformanceAdmin)


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
