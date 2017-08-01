"""
This generates a csv file brent_task.csv which is the raw task.csv
with additional columns: csr_treatment, seconds worked, day number, and wage

In order to run this code or any other scripts found in this directory, you must activate the virtualenvironment built in this
file's directory.

$ source venv/bin/activate
"""

import csv, os
import website.wsgi
from django.conf import settings
from django.contrib.auth.models import User
from data.models import Treatment, Task

BASE_DIR = getattr(settings, 'BASE_DIR', None)


def import_csv(filename):
    with open(os.path.join(BASE_DIR, filename), 'rb') as f:
        creader = csv.reader(f)
        headers = next(creader)
        out = []
        for row in creader:
            out.append(row)
    return out, headers

def get_headers(model=Task):
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
            row = [getattr(obj, h) for h in headers]
            day = int(obj.get_day())
            try:
                csr_treatment = obj.user.treatment.frameorder[day]
            except IndexError:
                csr_treatment = "NA"
            wage = obj.user.treatment.wage
            seconds_worked = get_seconds_worked(worktimer, obj.id)
            row += [csr_treatment, day, wage, seconds_worked]
            writer.writerow(row)


def main():
    worktimer, worktimerheaders = import_csv('worktimer_fix.csv')
    outFile = 'brent_task.csv'
    write_csv(outFile, Task, worktimer)


if __name__ == "__main__":
    main()
