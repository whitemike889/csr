from .models import Image, Task, WorkTimer, EventLog
from django.shortcuts import render

def timeout_logging(view_func):
    def _wrapped_view_func(request, image_id, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'login.html', {'message': "logged out due to inactivity"})
        if request.method == "POST":
            print request.POST['token']
            print request.POST['seconds']
            worktimer, created = WorkTimer.objects.get_or_create(user_id=request.user.id, value=request.POST['seconds'], token=request.POST['token'])
            task = Task.objects.get(user_id=request.user.id, image_id=image_id)
            eventlog = EventLog(task_id=task.id, name=request.POST['action'])
            eventlog.save()
        return view_func(request, image_id, *args, **kwargs)
    return _wrapped_view_func
