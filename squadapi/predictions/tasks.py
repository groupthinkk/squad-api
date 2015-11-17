from functools import partial
from statistics import mean

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import TurkerPerformance, InstagramPrediction, HIT, InstagramPost


logger = get_task_logger(__name__)


@shared_task
def update_turker_performance(turker):
    predictions = InstagramPrediction.objects.filter(
        hit__in=turker.hit_set.all()
    ).order_by('-created_datetime')[:300]

    correctness = mean(
        map(
            lambda x: x.correct,
            filter(lambda x: not x.contains_target, predictions),
        )
    )

    performance, created = TurkerPerformance.objects.get_or_create(
        turker=turker,
        defaults={'correctness': correctness},
    )

    if not created:
        performance.correctness = correctness
        performance.save()


def is_majority(hits, target_post, comparison):
    predictions = InstagramPrediction.objects.filter(
        hit__in=hits.all(),
        comparison=comparison,
    ).all()

    total_count = predictions.count()
    chosen_count = predictions.filter(choice=target_post).count()

    return chosen_count / total_count > 0.5


@shared_task
def update_hit_prediction(hit_id):
    hits = HIT.objects.filter(hit_id=hit_id)
    queue = hits.first().instagram_queue

    post_queryset = InstagramPrediction.choice.get_queryset()

    try:
        target_post = post_queryset.get(post_id=queue.name.lstrip('auto-'))
    except post_queryset.model.DoesNotExist:
        return

    relevant_comparisons = sorted(
        filter(lambda x: x.contains_post(target_post), queue.comparisons.all()),
        key=lambda z: z.opposite_post(target_post).likes_count,
    )

    if len(relevant_comparisons) != 3:
        return

    A, B, C = map(
        partial(is_majority, hits, target_post),
        relevant_comparisons,
    )

    likes_A, likes_B, likes_C = map(
        lambda x: x.opposite_post(target_post).likes_count,
        relevant_comparisons,
    )

    if not B and not A:
        lower_bound = 0
        upper_bound = likes_A
    elif not B and A:
        lower_bound = likes_A
        upper_bound = likes_B
    elif B and not C:
        lower_bound = likes_B
        upper_bound = likes_C
    elif B and C:
        lower_bound = likes_C
        upper_bound = 10 ** 10

    instagram_post, created = InstagramPost.objects.get_or_create(
        post=target_post,
        hit_id=hit_id,
        defaults={'lower_bound': lower_bound, 'upper_bound': upper_bound},
    )

    if not created:
        instagram_post.lower_bound = lower_bound
        instagram_post.upper_bound = upper_bound
        instagram_post.save()
