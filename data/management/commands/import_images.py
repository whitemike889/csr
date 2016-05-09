from django.core.management.base import BaseCommand, CommandError
from data.models import Image
from django.conf import settings
import csv, os

class Command(BaseCommand):
    help = "Imports the menulist.csv file to the database"

    def handle(self, *args, **options):
        for x in range(1,121):
            image, created = Image.objects.get_or_create(filename="steet_{}.png".format(x))
            image.save()


