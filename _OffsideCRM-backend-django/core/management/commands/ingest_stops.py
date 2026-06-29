from datetime import datetime
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from core.models import Stop

class Command(BaseCommand):
    help = 'Create stops from JSON file'

    def handle(self, *args, **kwargs):
        # set the path to the datafile
        datafile = settings.BASE_DIR / 'data' / 'stops.json'
        assert datafile.exists()

        # load the datafile
        with open(datafile, 'r') as f:
            data = json.load(f)
        
        # create tz-aware datetime object from the JSON string.
        DATE_FMT = "%Y-%m-%d %H:%M:%S"
        for stop in data:
            origin_window_range_start = datetime.strptime(stop['origin_window_range_start'], DATE_FMT)
            stop['origin_window_range_start'] = make_aware(origin_window_range_start)
            
            destination_window_range_start = datetime.strptime(stop['destination_window_range_start'], DATE_FMT)
            stop['destination_window_range_start'] = make_aware(destination_window_range_start)

        # convert list of dictionaries to list of Track models, and bulk_create
        stops = [Stop(**stop) for stop in data]

        Stop.objects.bulk_create(stops)