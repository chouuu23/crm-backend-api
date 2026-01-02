from django.core.management.base import BaseCommand
from accounts.models import Table

class Command(BaseCommand):
    help = "Create demo tables (2-6 seats) if none exist."

    def handle(self, *args, **options):
        if Table.objects.exists():
            self.stdout.write("Tables already exist, skipping.")
            return

        number = 1
        # create some sample tables
        sample = [
            (2, 2), (2, 3),    # two 2-seat tables and one 3-seat
            (3, 4), (4, 5),    # etc
            (4, 6), (4, 7),
            (5, 8), (6, 9),
        ]
        for seats, _num in sample:
            Table.objects.create(number=number, seats=seats)
            number += 1

        self.stdout.write("Demo tables created.")
