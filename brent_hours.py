"""
This generates a csv file brent_hours.csv which the ammount of
with additional columns: csr_treatment, seconds worked, day number, and wage

In order to run this code or any other scripts found in this directory, you must activate the virtualenvironment built in this
file's directory.

$ source venv/bin/activate
"""

import csv, os
import website.wsgi
from django.conf import settings
from django.contrib.auth.models import User
from data.models import Treatment, Constants
from datetime import timedelta as td

BASE_DIR = getattr(settings, 'BASE_DIR', None)


def get_work_for_day(daynumber, user, worktimer):
    workdates = Constants.workdates[user.treatment.batch]
    s = workdates['start']
    e = workdates['end']
    delta = e - s
    currDay = s + td(days=daynumber)
    currdayTaskFinish = user.task_set.filter(timefinished__date=currDay.date())
    taskIdList = [task.id for task in currdayTaskFinish]

    timeworked = []
    for task_id in taskIdList:
        timeworked.append(get_seconds_worked(worktimer, task_id))

    return sum(timeworked)



def import_csv(filename):
    with open(os.path.join(BASE_DIR, filename), 'rb') as f:
        creader = csv.reader(f)
        headers = next(creader)
        out = []
        for row in creader:
            out.append(row)
    return out, headers

def get_headers(model=Treatment):
    headers = []
    headers.append('user')
    q = model.objects.values()[0]
    for key, value in  q.items():
        headers.append(key)
    return headers

def get_seconds_worked(worktimer, task_id):
    seconds = list(filter(lambda row: row[2] == str(task_id), worktimer))
    return sum([int(row[4]) for row in seconds])

def write_csv(filename, model, worktimer):
    with open(filename, 'w') as f:
        writer = csv.writer(f, csv.excel)
        headers = get_headers(model)
        headersFull = headers + ['csr_treatment', 'day', 'wage', 'seconds_worked']
        writer.writerow(headersFull)
        for obj in model.objects.all():
            for daynumber in range(len(obj.frameorder)):
                row = [getattr(obj, h) for h in headers]
                seconds_worked = get_work_for_day(daynumber, obj.user, worktimer)
                csr_treatment = obj.frameorder[daynumber]
                wage = obj.wage
                row += [daynumber, csr_treatment, wage, seconds_worked]
                writer.writerow(row)


def main():
    worktimer, worktimerheaders = import_csv('worktimer_fix.csv')
    outFile = 'brent_hours.csv'
    write_csv(outFile, Treatment, worktimer)


if __name__ == "__main__":
    main()
