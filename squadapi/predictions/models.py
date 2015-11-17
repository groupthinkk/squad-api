from django.db import models
from django.core.exceptions import ValidationError


class Turker(models.Model):

    turker_id = models.CharField(max_length=128, unique=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.turker_id)


class TurkerPerformance(models.Model):

    turker = models.OneToOneField(Turker)
    correctness = models.FloatField(db_index=True)
    updated_datetime = models.DateTimeField(auto_now=True)


class HIT(models.Model):

    hit_id = models.CharField(max_length=128, db_index=True)
    turker = models.ForeignKey(Turker, to_field='turker_id')
    status = models.CharField(max_length=64, default='', blank=True, db_index=True)
    instagram_queue = models.ForeignKey('instagram.PostComparisonQueue')
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('hit_id', 'turker'), ('turker', 'instagram_queue'))


class InstagramPrediction(models.Model):

    hit = models.ForeignKey(HIT)
    comparison = models.ForeignKey('instagram.PostComparison')
    choice = models.ForeignKey('instagram.Post')
    decision_milliseconds = models.IntegerField()
    correct = models.BooleanField()
    ux_id = models.CharField(max_length=64, default='')
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hit', 'comparison')

    def clean(self):
        if self.choice_id not in (
            self.comparison.post_a_id,
            self.comparison.post_b_id,
        ):
            raise ValidationError('Choice must be within the comparison.')

    @property
    def contains_target(self):
        queue_name = self.hit.instagram_queue.name
        if 'auto' not in queue_name:
            return False
        return (
            self.comparison.post_a.post_id in queue_name
            or self.comparison.post_b.post_id in queue_name
        )
