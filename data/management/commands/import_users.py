from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from data.models import Treatment
from django.conf import settings
import csv, os
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Imports user.csv to database"

    def handle(self, *args, **options):
        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        csvDir = os.path.join(BASE_DIR, 'import-items')
        with open(os.path.join(csvDir, 'users.csv'), 'rb') as f:
            mycsv = csv.reader(f)
            next(mycsv, None)
            for row in mycsv:
                usr, created = User.objecst.get_or_create(username=row[0])
                usr.set_password("{}".format(row[1]))
                usr.save()
                treat, created = Treatment.objects.get_or_create(user_id=usr.id)
                treat.wage = row[2]
                treat.timezone = row[3]
                treat.batch = row[4]
                treat.assignment = row[5]
                treat.frameorder = row[6]
                treat.save()

