import json

from random import sample
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


HOT_15 = [
    'patagonia',
    'jcrew',
    'gap',
    'hm',
    'forever21',
    'zara',
    'nordstrom',
    'underarmour',
    'americaneagle',
    'topshop',
    'tommyhilfiger',
    'levis',
    'oldnavy',
    'abercrombie',
    'ralphlauren',
]


@shared_task
def update_user(user):
    user_data = get_user(user.user_id)

    user.name = user_data['full_name']
    user.username = user_data['username']
    user.followers = user_data['counts']['followed_by']
    user.image_url = user_data['profile_picture']
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


def get_post_comparisons(user, post):
    posts = Post.objects.filter(user=user).order_by('-created_datetime')[10:50]

    sorted_posts = sorted(posts, key=attrgetter('likes_count'))

    i1 = int(len(sorted_posts) * 1 / 4)
    i2 = int(len(sorted_posts) * 2 / 4)
    i3 = int(len(sorted_posts) * 3 / 4)

    v1 = sorted_posts[max(0, i1 - 2):i1 + 1]
    v2 = sorted_posts[max(0, i2 - 2):i2 + 1]
    v3 = sorted_posts[max(0, i3 - 2):i3 + 1]

    def minimize_time_of_day_error(posts):
        return sum([
            min(p.created_datetime.hour, 24 - p.created_datetime.hour)
            for p in posts
        ]) / len(posts)

    posts = sorted(product(v1, v2, v3), key=minimize_time_of_day_error)[0]

    return combinations(chain(posts, [post]), 2)


@shared_task
def update_comparison_queue(user, queue, post_id):
    users = User.objects.filter(username__in=sample(HOT_15, 5))

    for u in chain([user], users):
        update_user_posts(u, count=50)

        if u == user:
            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                return
        else:
            post = Post.objects.filter(user=u).order_by(
                '-created_datetime',
            ).first()

        for post_a, post_b in get_post_comparisons(u, post):
            comparison, _ = PostComparison.objects.get_or_create(
                post_a=post_a,
                post_b=post_b,
                defaults={'user': u},
            )
            member = PostComparisonQueueMember(
                queue=queue,
                comparison=comparison,
            )
            member.save()
