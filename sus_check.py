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
        addlist = []
        removelist = []
        if len(timers) > 1:
            for x in range(len(timers)-1):
                v = timers[x].value
                if timers[x].timestamp - timedelta(seconds=v) < timers[x+1].timestamp:
                    count += 1
                    remove = v
                    add = timers[x].timestamp - timers[x+1].timestamp
                    print t.user, timers[x].token, remove, add.seconds, timers[x].timestamp
                    addlist.append(add.seconds)
                    removelist.append(remove)
        worktime = sum([t.value for t in timers])
        userDict.append([t.user, count, len(t.user.task_set.all()), worktime, sum(addlist), sum(removelist), worktime - sum(removelist) + sum(addlist)])

with open('overview.csv', 'w') as f:
    writer = csv.writer(f, csv.excel)
    writer.writerow(['user', 'occurance', 'tasks', 'worktime_raw', 'addvalues', 'removevalues', 'worktime'])
    for u in userDict:

        writer.writerow(u)



