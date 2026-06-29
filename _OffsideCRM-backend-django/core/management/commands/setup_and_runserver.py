from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.models import Country, TruckType


class Command(BaseCommand):
    help = 'Seeds the database with required data and runs the development server.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            default='8000',
            help='Port to run the development server on (default: 8000)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Step 1: Running migrations...'))
        call_command('migrate', verbosity=1)

        self.stdout.write(self.style.MIGRATE_HEADING('\nStep 2: Seeding required data...'))
        self._seed_countries()
        self._seed_truck_types()

        self.stdout.write(self.style.MIGRATE_HEADING('\nStep 3: Starting development server...'))
        port = options['port']
        call_command('runserver', f'127.0.0.1:{port}')

    def _seed_countries(self):
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
                self.stdout.write(self.style.SUCCESS(f'  Created country: {name} ({iso_code})'))
            else:
                self.stdout.write(f'  Country already exists: {name} ({iso_code})')

    def _seed_truck_types(self):
        truck_types = [
            'None',
            'Semi',
            'Box',
            'Flatbed',
            'Reefer',
            'Dry Van',
            'Tanker',
            'Step Deck',
            'Hotshot',
        ]
        for name in truck_types:
            tt, created = TruckType.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created truck type: {name}'))
            else:
                self.stdout.write(f'  Truck type already exists: {name}')
