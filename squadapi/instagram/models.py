from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):

    user_id = models.CharField(max_length=64, default='', blank=True)
    username = models.CharField(max_length=64, unique=True)
    followers = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):

    user = models.ForeignKey(User)
    post_id = models.CharField(max_length=64, unique=True)
    caption = models.TextField()
    image_url = models.URLField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(db_index=True)

    def image_tag(self):
        return '<img src="{0}" width="50"/>'.format(self.image_url)
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'


class Normalization(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    data = models.TextField()


class PostComparison(models.Model):

    user = models.ForeignKey(User)
    post_a = models.ForeignKey(Post, related_name='post_a')
    post_b = models.ForeignKey(Post, related_name='post_b')

    class Meta:
        unique_together = ('post_a', 'post_b')

    def clean(self):
        if not self.post_a.user == self.post_b.user:
            raise ValidationError('Post comparisons must have the same user.')
        self.user = self.post_a.user

    @property
    def summary_template(self):
        return (
            '<img src="{}" width="50" style="float: left;margin-right: 10px"/>'
            '<div>{}</div>'
        )

    def post_a_summary(self):
        return self.summary_template.format(
            self.post_a.image_url,
            self.post_a.caption,
        )
    post_a_summary.allow_tags = True
    post_a_summary.short_description = 'Post A'

    def post_b_summary(self):
        return self.summary_template.format(
            self.post_b.image_url,
            self.post_b.caption,
        )
    post_b_summary.allow_tags = True
    post_b_summary.short_description = 'Post B'

    def __str__(self):
        return '{} {}, {} {}'.format(
            self.post_a.user,
            self.post_a.created_datetime.strftime('%m-%d-%y %H:%M'),
            self.post_b.user,
            self.post_b.created_datetime.strftime('%m-%d-%y %H:%M'),
        )


class PostComparisonQueue(models.Model):

    name = models.CharField(max_length=128)
    comparisons = models.ManyToManyField(
        PostComparison,
        through='PostComparisonQueueMember',
        through_fields=('queue', 'comparison'),
    )


class PostComparisonQueueMember(models.Model):

    queue = models.ForeignKey(PostComparisonQueue)
    comparison = models.ForeignKey(PostComparison)
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('queue', 'comparison')
