from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Image, Task, EventLog
from django.forms.models import inlineformset_factory, modelform_factory
from .decorators import timeout_logging
from forms import MenuItemForm
from django.db import models
from django import forms
from django.conf import settings
import user_patch

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    return HttpResponseRedirect(reverse('data:images'))


@login_required(login_url="/login/")
def list_images(request):
    images = request.user.get_tasks()
    context = {
        'images': images,
    }
    return render(request, "data/images.html", context)


def field_widget_callback(field):
    return forms.TextInput(attrs={'placeholder': field.name})

@timeout_logging
def task_entry(request, image_id):
    fields = [
        'month','year','street', 'citystate', 'pic_quality', 'str_quality', 'pot_holes',
        'bui_quality', 'car_quality', 'litter', 'road_work', 'for_sale',
        'shoes', 'people', 'broken_signs', 'trees',
    ]
    inactive = 0
    task, created = Task.objects.get_or_create(image_id=image_id, user_id=request.user.id)
    TaskForm = modelform_factory(Task, exclude=['id', 'image', 'user', 'finished', 'timestarted', 'timefinished',])
    # Evaluate which form the post came from.  If from timer, then repopulate with request.DATA
    # else save it per usual
    if request.method == "POST":
        taskform = TaskForm(request.POST, request.FILES, instance=task)
        if request.POST['action'] == "save":
            for f in fields:
                val = request.POST[f]
                if val != '':
                    if f != 'street' and f != 'citystate':
                        val = int(val)
                    setattr(task,f, val)
            task.save()
        if request.POST['action'] == "submit":
            if taskform.is_valid():
                task.finished = 1
                task.save()
                return HttpResponseRedirect(reverse('data:images'))

        if request.POST['action'] == "log":
            inactive = 1

    else:
        taskform = TaskForm(instance=task)


    context = {
        'inactive': inactive,
        'task': task,
        'taskform': taskform,
        'DEBUG': settings.DEBUG,
    }
    return render(request, "data/task_entry.html", context)

@login_required(login_url="/login/")
def log_event(request, image_id):
    task = Task.objects.get(image_id=image_id, user_id=request.user.id)
    url = "/taskentry/{}".format(task_id)
    event = EventLog(task_id=task.id, name="timeout")
    event.save()
    return redirect(url)
