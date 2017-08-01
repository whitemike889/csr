from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from data.models import Treatment
from django.conf import settings
from datetime import date, timedelta as td
import csv, os

class Command(BaseCommand):
    help = "Exports task and tracking data"

    def get_headers(self, model=Treatment):
        headers = []
        headers.append('user')
        q = model.objects.values()[0]
        for key, value in  q.items():
            headers.append(key)
        return headers

    def write_csv(self, filename, model):
        with open(filename, 'w') as f:
            writer = csv.writer(f, csv.excel)
            headers = self.get_headers(model)
            writer.writerow(headers)
            for obj in model.objects.all():
                row = [getattr(obj, h) for h in headers]
                if model._meta.object_name =="User":
                    worktime = sum([x.value for x in obj.worktimer_set.all()])
                    row = row + [worktime]
                writer.writerow(row)

    def handle(self, *args, **options):
        exportDir = os.path.join(settings.BASE_DIR, 'export')
        if not os.path.isdir(exportDir):
            os.mkdir(exportDir)

        treatmentFile = os.path.join(exportDir, 'treatments.csv')
        self.write_csv(treatmentFile, Treatment)



