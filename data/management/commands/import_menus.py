from django.core.management.base import BaseCommand, CommandError
from data.models import Menu
from django.conf import settings
import csv, os

class Command(BaseCommand):
    help = "Imports the menulist.csv file to the database"

    def handle(self, *args, **options):
        filename = os.path.join(settings.BASE_DIR,'menulist.csv')
        with open(filename) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                menu, created = Menu.objects.get_or_create(filename=row[0])
                menu.save()


