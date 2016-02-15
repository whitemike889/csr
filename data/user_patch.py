from django.contrib.auth.models import User
from .models import Image, Task

def get_billable_hours(self):
    worktimers = self.worktimer_set.all()
    m, s = divmod(sum([x.value for x in worktimers]), 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

User.add_to_class('get_billable_hours', get_billable_hours)

def get_tasks(self):
    notStarted = []
    unfinished = []
    sIds = []
    finished = []
    for task in Task.objects.filter(user_id=self.id):
        if task.finished == 1:
            finished.append(task)
        else:
            unfinished.append(task)
        sIds.append(task.image.id)

    for image in Image.objects.all():
        if image.id not in sIds:
            notStarted.append(image)

    return dict(notStarted=notStarted, unfinished=unfinished, finished=finished)

User.add_to_class('get_tasks', get_tasks)

def __str__(self):
    return self.username

User.add_to_class('__str__', __str__)

