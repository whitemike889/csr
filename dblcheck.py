import csv, os
import website.wsgi
from django.conf import settings
from django.contrib.auth.models import User
from random import shuffle

BASE_DIR = getattr(settings, 'BASE_DIR', None)
CHK_DIR = os.path.join(BASE_DIR,'dblcheck')
def import_csv(filename):
    with open(os.path.join(CHK_DIR, filename), 'rb') as f:
        creader = csv.reader(f)
        next(creader, None)
        out = []
        for row in creader:
            out.append(row)
    return out

prod = import_csv('data_struct_prod.csv')

#add task_index
idx = 0
prod[0].append(idx)
for i in range(1,len(prod)):
    if prod[i-1][4] == prod[i][4]:
        idx += 1
    else:
        idx = 0
    prod[i].append(idx)


users = import_csv('USERS.csv')

# clean users
userDict = {}
for r in users:
    userDict[int(r[1])] = r[0].replace("'",'')



# get usersnames for prod
for row in prod:
    row.append(userDict[int(row[4])])

# check frame and minutes
# 11 or 15 from DB
csr_errors = 0
time_errors = 0

usrs = User.objects.all()


# this is not a good mapping between the two data sets
shuffle(prod)
for row in prod[:100]:
    usr = usrs.filter(username=row[-1])[0]
    tasks = usr.task_set.order_by('id')
    task = tasks[row[-2]]
    wt = task.worktimer_set.all()
    seconds = sum(x.value for x in wt)
    #frame = usr.treatment.get_frame_retro(task.timefinished)
    events = task.eventlog_set.all()
    frames = [int(e.frame) - 1 for e in events]
    #frame = usr.treatme]
    if int(row[0]) not in frames:
        csr_errors += 1
        #print errors
    if abs(int(seconds) - float(row[8])) > 3:
        time_errors += 1

print "Errors in csr_treatment: {}".format(csr_errors)
print "Errors in seconds_production: {}".format(time_errors)





## compare number of tasks in prod vs my data
# user, day, prod_no, db_no
outData =  []
for key, value in userDict.items():
    usr = User.objects.get(username=value)
    userProd = list(filter(lambda row: int(row[4]) == int(key), prod))
    for day in range(len(usr.treamtment.frameorder)):
        dayList = list(filter(lambda row: int(row[2]) == day, userProd))
        row = [value, day, len(dayList), usr.treatment.get_number_of_tasks(day)]
        outData.append(row)


## writecsv

hours = import_csv('data_struct_hours.csv')

for row in hours:
    row.append(userDict[int(row[4])])
wage_errors = 0
csr_errors = 0


#shuffle(hours)
errorsDict = [{},{}]
for row in hours:
    usr = usrs.filter(username=row[-1])[0]
    trtwage = usr.treatment.wage
    if int(trtwage) == 11:
        wage = 0
    elif int(trtwage) == 15:
        wage = 1
    else:
        pass
    if wage != int(row[5]):
        wage_errors += 1
        try:
            errorsDict[0][usr.treatment.batch] = errorsDict[0][usr.treatment.batch] + 1
        except KeyError:
            errorsDict[0][usr.treatment.batch] = 1

    frame = usr.treatment.frameorder[int(row[2])-1]
    if int(frame)-1 != int(row[0]):
        csr_errors += 1
        print usr.treatment.batch
        try:
            errorsDict[1][usr.treatment.batch] = errorsDict[1][usr.treatment.batch] + 1
        except KeyError:
            errorsDict[1][usr.treatment.batch] = 1


print "Errors in csr_treatment: {}".format(csr_errors)
print "Errors in high_wage: {}".format(wage_errors)


for row in errorsDict:
    print row


## compare number of tasks in prod vs my data


