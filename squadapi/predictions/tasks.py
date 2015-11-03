from statistics import mean

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import TurkerPerformance, InstagramPrediction


logger = get_task_logger(__name__)


@shared_task
def update_turker_performance(turker):
    hit = turker.hit_set.order_by('-created_datetime').first()
    predictions = InstagramPrediction.objects.filter(hit=hit)
    correctness = mean(predictions.values_list('correct', flat=True))

    performance, created = TurkerPerformance.objects.get_or_create(
        turker=turker,
        defaults={'correctness': correctness},
    )

    if not created:
        performance.correctness = sum(correct) / len(correct)
        performance.save()
