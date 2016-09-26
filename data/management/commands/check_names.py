from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from data.models import Treatment
from django.conf import settings
import csv, os
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Checks user.csv for duplicate usernames"

    def handle(self, *args, **options):
        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        csvDir = os.path.join(BASE_DIR, 'import-items')
        with open(os.path.join(csvDir, 'users.csv'), 'rb') as f:
            mycsv = csv.reader(f)
            next(mycsv, None)
            for row in mycsv:
                try:
                    usr = User.objects.get(username=row[0])
                    print "Warning: username already exists:    {}".format(usr.username)
                except User.DoesNotExist:
                    pass
            print "Finished"


