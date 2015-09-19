from django.db import models
from django.core.exceptions import ValidationError


class Turker(models.Model):

    turker_id = models.CharField(max_length=128, unique=True)
    instagram_queue = models.ForeignKey(
        'instagram.PostComparisonQueue',
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{}'.format(self.turker_id)


class InstagramPrediction(models.Model):

    turker = models.ForeignKey(Turker)
    comparison = models.ForeignKey('instagram.PostComparisonQueueMember')
    choice = models.ForeignKey('instagram.Post', to_field='post_id')
    decision_milliseconds = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    def clean(self):
        comparison = self.comparison.comparison
        if not self.choice in (comparison.post_a, comparison.post_b):
            raise ValidationError('Choice must be a member of the comparison.')
