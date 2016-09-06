from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from data.models import Task, WorkTimer, EventLog, Constants
from django.conf import settings
from datetime import date, timedelta as td
import csv, os

class Command(BaseCommand):
    help = "Exports task and tracking data"

    def get_headers(self, model):
        headers = []
        if model._meta.object_name != "EventLog" and model._meta.object_name != "User":
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
                writer.writerow(row)

    def get_margin_worked(self, user):
        workdates = Constants.workdates[user.treatment.batch]
        s = workdates['start']
        e = workdates['end']
        #build headers of day1 day2 ... dayN
        delta = e - s
        print delta
        row = []
        row.append(user.username)
        for i in range(delta.days + 1):
            currDay = s + td(days=i)
            currdayEvents = user.eventlog_set.filter(timestamp__date=currDay.date())
            eventNameList = [x.name for x in currdayEvents]
            dayXlogin = "login" in eventNameList
            currdayTaskStart = user.task_set.filter(timestarted__date=currDay.date())
            currdayTaskFinish = user.task_set.filter(timefinished__date=currDay.date())
            dayXwork = len(set([x.id for x in currdayTaskStart] + [x.id for x in currdayTaskFinish]))
            row.append(dayXlogin)
            row.append(dayXwork)
        return row

        #look for logins
        #look for tasks started

    def handle(self, *args, **options):
        exportDir = os.path.join(settings.BASE_DIR, 'export')
        if not os.path.isdir(exportDir):
            os.mkdir(exportDir)

        taskFile = os.path.join(exportDir, 'task.csv')
        self.write_csv(taskFile, Task)

        eventFile = os.path.join(exportDir, 'eventlog.csv')
        self.write_csv(eventFile, EventLog)

        workFile = os.path.join(exportDir, 'worktimer.csv')
        self.write_csv(workFile, WorkTimer)

        userFile = os.path.join(exportDir, "user.csv")
        self.write_csv(userFile, User)

        marginWorkFile = os.path.join(exportDir, "marginwork.csv")
        rows = []
        for user in User.objects.all():
            rows.append(self.get_margin_worked(user))
        length = max([len(x) for x in rows])
        headers =['user_id']
        for x in range(length/2):
            headers.append("day{}Login".format(x))
            headers.append("day{}Work".format(x))
        with open(marginWorkFile, 'w') as f:
            writer = csv.writer(f, csv.excel)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)



