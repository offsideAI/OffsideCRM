from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Seeds the database with required reference data (Countries, etc.).'

    def handle(self, *args, **options):
        self.stdout.write('Seeding required reference data...')

        countries = [
            ('USA', 'United States'),
            ('CAN', 'Canada'),
            ('MEX', 'Mexico'),
        ]
        for iso_code, name in countries:
            country, created = Country.objects.get_or_create(
                iso_code=iso_code,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(f'  Created country: {name} ({iso_code})')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
