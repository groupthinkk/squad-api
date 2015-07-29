from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import User, Post
from .collect import get_posts


logger = get_task_logger(__name__)


@shared_task
def update_all_posts(user):
    logger.info('THIS FUNCTION CHANGED')
    return
    for post in get_posts(user.user_id):
        try:
            p = Post.objects.get(post_id=post['id'])
        except Post.DoesNotExist:
            p = Post(
                user=user,
                post_id=post['id'],
                caption=(post['caption'] or {}).get('text') or '',
                created_datetime=datetime.fromtimestamp(int(post['created_time'])),
            )
        p.caption = (post['caption'] or {}).get('text') or ''
        p.likes_count = post['likes']['count']
        p.comments_count = post['comments']['count']
        p.save()
