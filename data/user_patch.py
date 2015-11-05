from django.contrib.auth.models import User

def get_billable_hours(self):
    worktimers = self.worktimer_set.all()
    return sum([x.value for x in worktimers])

User.add_to_class('get_billable_hours', get_billable_hours)
