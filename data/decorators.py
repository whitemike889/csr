from .models import EventLog, MenuEntry

def timeout_logging(view_func):
    def _wrapped_view_func(request, menu_id, *args, **kwargs):
        if request.method == "POST":
            if request.POST['action'] == "log":
                menuentry = MenuEntry.objects.get(user_id=request.user.id, menu_id=menu_id)
                eventlog = EventLog(menuentry_id=menuentry.id, name='timeout')
                eventlog.save()
        return view_func(request, menu_id, *args, **kwargs)
    return _wrapped_view_func
