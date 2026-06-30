from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Prints all environment variables'

    def handle(self, *args, **kwargs):
        for key, value in os.environ.items():
            self.stdout.write(f"{key}: {value}")