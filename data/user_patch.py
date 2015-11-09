from django.contrib.auth.models import User

def get_billable_hours(self):
    worktimers = self.worktimer_set.all()
    m, s = divmod(sum([x.value for x in worktimers]), 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

User.add_to_class('get_billable_hours', get_billable_hours)
