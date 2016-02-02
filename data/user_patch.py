from django.contrib.auth.models import User
from .models import Image, Task

def get_billable_hours(self):
    worktimers = self.worktimer_set.all()
    m, s = divmod(sum([x.value for x in worktimers]), 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

User.add_to_class('get_billable_hours', get_billable_hours)

def get_tasks(self):
    unfinished = []
    finished = []
    for image in Image.objects.all():
        task = Task.objects.get(user_id=self.id, image_id=image.id)
        if task.finished == 1:
            finished.append(task)
        else:
            unfinished.append(task)
    return dict(unfinished=unfinished, finished=finished)

User.add_to_class('get_tasks', get_tasks)

