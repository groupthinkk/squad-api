import json

from datetime import datetime
from operator import attrgetter
from itertools import product, combinations, chain
from statistics import mean, stdev
from collections import defaultdict

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import (
    User, Post, Normalization, PostComparison, PostComparisonQueueMember,
)
from .collect import get_user, get_posts


logger = get_task_logger(__name__)


@shared_task
def update_user(user):
    user_data = get_user(user.user_id)

    user.username = user_data['username']
    user.followers = user_data['counts']['followed_by']
    user.save()


@shared_task
def update_user_posts(user, **kwargs):
    for post in get_posts(user.user_id, **kwargs):
        try:
            p = Post.objects.get(post_id=post['id'])
        except Post.DoesNotExist:
            p = Post(
                user=user,
                post_id=post['id'],
                caption=(post['caption'] or {}).get('text') or '',
                image_url=post['images']['standard_resolution']['url'],
                created_datetime=datetime.fromtimestamp(int(post['created_time'])),
            )
        p.caption = (post['caption'] or {}).get('text') or ''
        p.image_url = post['images']['standard_resolution']['url']
        p.likes_count = post['likes']['count']
        p.comments_count = post['comments']['count']
        p.save()


@shared_task
def update_normalization_data(user):
    data = dict()
    likes = defaultdict(list)

    for post in Post.objects.filter(user=user).order_by('-created_datetime'):
        likes[post.created_datetime.year].append(post.likes_count)

    for year, counts in likes.items():
        data[year] = {
            'mean': mean(counts),
            'stdev': stdev(counts),
        }

    updated_values = {'data': json.dumps(data)}

    Normalization.objects.update_or_create(user=user, defaults=updated_values)


def select_comparison_posts(user):
    posts = Post.objects.filter(user=user).order_by('-created_datetime')[10:50]

    sorted_posts = sorted(posts, key=attrgetter('likes_count'))

    i1 = int(len(sorted_posts) * 1 / 4)
    i2 = int(len(sorted_posts) * 2 / 4)
    i3 = int(len(sorted_posts) * 3 / 4)

    v1 = sorted_posts[max(0, i1 - 2):i1 + 1]
    v2 = sorted_posts[max(0, i2 - 2):i2 + 1]
    v3 = sorted_posts[max(0, i3 - 2):i3 + 1]

    mean_squared_error = lambda x: sum([i.likes_count for i in x]) / len(x)

    return sorted(product(v1, v2, v3), key=mean_squared_error)[0]


@shared_task
def update_comparison_queue(user, queue, post_id):
    update_user_posts(user, count=50)

    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return

    comparison_posts = select_comparison_posts(user)

    for post_a, post_b in combinations(chain(comparison_posts, [post]), 2):
        comparison, _ = PostComparison.objects.get_or_create(
            post_a=post_a,
            post_b=post_b,
            defaults={'user': user},
        )
        member = PostComparisonQueueMember(
            queue=queue,
            comparison=comparison,
        )
        member.save()
