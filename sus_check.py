import website.wsgi

from data.models import Treatment
from datetime import timedelta
import csv

userDict = []
with open('differences.csv', 'w') as f:
    writer = csv.writer(f, csv.excel)
    writer.writerow(['user', 'difference', 'page'])
    for t in Treatment.objects.all():
        timers = t.user.worktimer_set.order_by('-timestamp')
        count = 0
        if len(timers) > 1:
            for x in range(len(timers)-1):
                v = timers[x].value
                diffStamps = timers[x].timestamp - timers[x+1].timestamp
                if diffStamps < timedelta(seconds=30):
                    diff = v - diffStamps.seconds
                    if  diff > 2:
                        count += 1
                        writer.writerow([t.user, diff, timers[x].page])
        userDict.append([t.user, count, len(t.user.task_set.all())])

with open('overview.csv', 'w') as f:
    writer = csv.writer(f, csv.excel)
    writer.writerow(['user', 'occurance', 'tasks'])
    for u in userDict:
        writer.writerow(u)



