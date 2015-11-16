from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Menu, MenuEntry, MenuItem, EventLog
from django.forms.models import inlineformset_factory, modelformset_factory
from .decorators import timeout_logging
from forms import MenuItemForm
from django.db import models
from django import forms
from django.conf import settings

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    return HttpResponseRedirect(reverse('data:menus'))


@login_required(login_url="/login/")
def list_menus(request):
    menuValues = Menu.objects.all().values()
    for menuObj in Menu.objects.all():
        finished = menuObj.check_status(request.user)
        menuVal = filter(lambda m: m['id']==menuObj.id, menuValues)[0]
        menuVal['finished'] = finished

    context = {
        'menus': menuValues,
    }

    return render(request, "data/menus.html", context)


def field_widget_callback(field):
    return forms.TextInput(attrs={'placeholder': field.name})


@timeout_logging
def menu_entry(request, menu_id):
    inactive = 0
    menu = Menu.objects.get(id=menu_id)
    MenuEntryFormset = modelformset_factory(MenuEntry, fields=('restaurantName', 'finished',), max_num=1)
    MenuItemFormset = inlineformset_factory(MenuEntry, MenuItem, MenuItemForm, extra=1)
    menuentry, created = MenuEntry.objects.get_or_create(user_id=request.user.id, menu_id=menu_id)
    menuQuery = MenuEntry.objects.filter(user_id=request.user.id, menu_id=menu_id)
    # Evaluate which form the post came from.  If from timer, then repopulate with request.DATA
    # else save it per usual
    if request.method == "POST":
        print "GUID: {}".format(request.POST['seconds'])
        entryformset = MenuEntryFormset(request.POST, request.FILES)
        itemformset = MenuItemFormset(request.POST, request.FILES, instance=menuentry)
        if request.POST['action'] == "+" or request.POST['action'] == "submit":
            if itemformset.is_valid() and entryformset.is_valid():
                entryformset.save()
                itemformset.save()
                if request.POST['action'] == "submit":
                    return HttpResponseRedirect(reverse('data:menus'))
                if request.POST['action'] == "+":
                    entryformset = MenuEntryFormset(queryset=MenuEntry.objects.filter(user_id=request.user.id, menu_id=menu_id))
                    itemformset = MenuItemFormset(instance=menuentry)
        if request.POST['action'] == "log":
            inactive = 1

    else:
        entryformset = MenuEntryFormset(queryset=MenuEntry.objects.filter(user_id=request.user.id, menu_id=menu_id))
        itemformset = MenuItemFormset(instance=menuentry)

    context = {
        'inactive': inactive,
        'menu': menu,
        'entryformset': entryformset,
        'itemformset': itemformset,
        'DEBUG': settings.DEBUG,
    }
    return render(request, "data/menu_entry.html", context)

@login_required(login_url="/login/")
def log_event(request, menu_id):
    menuentry = MenuEntry.objects.get(user_id=request.user.id, menu_id=menu_id)
    url = "/menuentry/{}".format(menu_id)
    event = EventLog(menuentry_id=menuentry.id, name="timeout")
    event.save()
    return redirect(url)
