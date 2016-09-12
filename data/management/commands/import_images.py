from django.core.management.base import BaseCommand, CommandError
from data.models import Image
from django.conf import settings
import csv, os

class Command(BaseCommand):
    help = "Imports the menulist.csv file to the database"

    def handle(self, *args, **options):
        ordN = sorted([x.order for x in Image.objects.all()])
        ordN = ordN[-1] + 1
        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        with open(os.path.join(BASE_DIR, 'imagelist.csv')) as f:
            creader = csv.reader(f)
            for x in creader:
                image, created = Image.objects.get_or_create(filename=x[0])
                if created:
                    image.order = ordN
                    ordN += 1
                image.save()


