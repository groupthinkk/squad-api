import json

from random import sample, randint
from datetime import datetime, date, timedelta
from operator import attrgetter
from itertools import product, chain
from statistics import mean, stdev
from collections import defaultdict

from celery import shared_task
from celery.utils.log import get_task_logger

from django.db import IntegrityError

from .models import (
    User, Post, Normalization, PostComparison, PostComparisonQueueMember, Follow,
)
from .collect import (
    get_user, get_posts, get_follows, InstagramAPIError, InstagramAPIRateLimit,
)


logger = get_task_logger(__name__)


COMPARISON_ACCOUNTS = [
    'jcrew',
    'hm',
    'underarmour',
    'levis',
    'ralphlauren',
]


@shared_task
def add_user(data):
    from .forms import UserAdminForm

    form = UserAdminForm(data)

    if form.is_valid():
        form.save(commit=True)


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
    posts = Post.objects.filter(
        user=user,
        created_datetime__lt=post.created_datetime,
    ).order_by('-created_datetime')[:30]

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

    return sorted(product(v1, v2, v3), key=minimize_time_of_day_error)[0]

def create_comps(num_posts, num_bins, comps_per_bin):
    # check if there are too many bins
    if num_bins > num_posts:
        return "Too many bins!"
    # break points in the distribution
    break_pts = [-1]
    for i in range(0, num_bins - 1):
        temp = (i + 1) * int(round(float(num_posts)/num_bins)) - 1
        break_pts.append(temp)

    # add the end point
    break_pts.append(num_posts - 1)

    # create a list of bins
    bins = []
    for i in range(0, len(break_pts) - 1):
        temp = []
        for j in range(break_pts[i] + 1, break_pts[i + 1] + 1):
            temp.append(j)
        bins.append(temp)
        # check if the bins are large enough
        if comps_per_bin > len(bins[i]):
            return "Too many comparisons per bin!"

    # create a list of comparisons
    comps = []
    for i in range(0, len(bins)):
        for j in range(0, comps_per_bin):
            # select a random element from the current bin
            val = bins[i][randint(0, len(bins[i]) - 1)]
            # add the value to the list
            comps.append(val)
            # remove the bin
            bins[i].remove(val)

    comps.sort()
    return comps

def new_queue(post_data, target_id, n_bins, comps_bin):

    n_rows = len(post_data)
    # create comparison indices
    comps = create_comps(n_rows, n_bins, comps_bin)

    # extract post ids
    p_id = [post_data[i].post_id for i in comps]

    return p_id

@shared_task
def update_comparison_queue(users, queue, post_ids):
    for i in range(len(users)):
        u = users[i]
        target_id = post_ids[i]
        #update_user_posts(u, count=150)
        posts = Post.objects.filter(user=u).exclude(
            created_datetime__gte=date.today()-timedelta(days=3)
            ).exclude(
            post_id = target_id
            ).order_by(
            'likes_count',
        )
        other_ids = new_queue(posts, target_id, 3, 1)
        for other_id in other_ids:
            post_a, post_b = sample(list(Post.objects.filter(post_id__in = [target_id, other_id])), 2)
            comparison, _ = PostComparison.objects.get_or_create(
                        post_a=post_a,
                        post_b=post_b,
                        defaults={'user': u},
                    )
            member = PostComparisonQueueMember(
                queue=queue,
                comparison=comparison,
            )
            try:
                member.save()
            except IntegrityError:
                pass

@shared_task
def update_user_follows(user, depth=2):
    if depth < 1:
        return

    for user_data, exception in get_follows(user.user_id):
        if exception:
            try:
                raise exception
            except InstagramAPIRateLimit:
                update_user_follows.apply_async(
                    args=[user, depth],
                    queue='crawler',
                    countdown=60 * 5,
                )
                raise exception

        try:
            follows_user = User.objects.get(user_id=user_data['id'])
        except User.DoesNotExist:
            follows_user = User(
                name=user_data['full_name'],
                user_id=user_data['id'],
                username=user_data['username'],
                image_url=user_data['profile_picture'],
            )
            follows_user.save()

        update_user_follows.apply_async(
            args=[follows_user, depth - 1],
            queue='crawler',
        )

        Follow.objects.get_or_create(user=user, follows_user=follows_user)
