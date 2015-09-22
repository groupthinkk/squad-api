from django.db import models
from django.core.exceptions import ValidationError


class Turker(models.Model):

    turker_id = models.CharField(max_length=128, unique=True)
    instagram_queue = models.ForeignKey(
        'instagram.PostComparisonQueue',
        blank=True,
        null=True,
    )
    updated_datetime = models.DateTimeField(auto_now=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.turker_id)


class InstagramPrediction(models.Model):

    turker = models.ForeignKey(Turker)
    comparison = models.ForeignKey('instagram.PostComparisonQueueMember')
    choice = models.ForeignKey('instagram.Post')
    decision_milliseconds = models.IntegerField()
    correct = models.BooleanField()
    ux_id = models.CharField(max_length=64, default='')
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('turker', 'comparison')

    def clean(self):
        if self.choice_id not in (
            self.comparison.comparison.post_a_id,
            self.comparison.comparison.post_b_id,
        ):
            raise ValidationError('Choice must be within the comparison.')
