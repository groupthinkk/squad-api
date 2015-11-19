import sys
import csv

from django.core.management.base import BaseCommand, CommandError

from predictions.models import Turker, InstagramPrediction, HIT


class Command(BaseCommand):

    help = 'Exports the specified HIT predictions to a CSV'

    def add_arguments(self, parser):
        parser.add_argument('hit_id', nargs='+', type=str)

    def handle(self, *args, **options):
        for hit_id in options['hit_id']:
            hit_exists = self.export_hit(hit_id)

            if not hit_exists:
                raise CommandError('HIT "{}" does not exist'.format(hit_id))

            self.stdout.write('Successfully exported hit "{}"'.format(hit_id))

    def format_row(self, hit, prediction):
        fmt = '%Y-%m-%dT%H:%M:%S.%f'

        return [
            hit.turker.turker_id,
            prediction.created_datetime.strftime(fmt),
            prediction.comparison.post_a.user.username,
            prediction.comparison.post_a,
            prediction.comparison.post_a.likes_count,
            prediction.comparison.post_a.created_datetime.strftime(fmt),
            prediction.comparison.post_b,
            prediction.comparison.post_b.likes_count,
            prediction.comparison.post_b.created_datetime.strftime(fmt),
            prediction.choice,
            int(prediction.decision_milliseconds / 1000),
        ]

    def generate_rows(self, hit_id):
        for hit in HIT.objects.filter(hit_id=hit_id):
            for p in hit.instagramprediction_set.order_by('created_datetime'):
                yield self.format_row(hit, p)

    def export_hit(self, hit_id):
        hit_exists = False

        with open('{}.csv'.format(hit_id), 'w', newline='') as fd:
            writer = csv.writer(fd)

            writer.writerow([
                'Turker ID',
                'Datetime',
                'Instagram Username',
                'Post A',
                'Post A Likes',
                'Post A Datetime',
                'Post B',
                'Post B Likes',
                'Post B Datetime',
                'Prediction Choice',
                'Decision Milliseconds',
            ])

            for row in self.generate_rows(hit_id):
                hit_exists = True
                writer.writerow(row)

        return hit_exists
