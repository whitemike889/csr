from django.contrib import admin
from .models import WorkTimer, MenuEntry, MenuItem
from django.contrib.auth.models import User
# Register your models here.

class TimeSheet(User):
    class Meta:
        proxy = True

@admin.register(WorkTimer)
class WorkTimerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'token', 'value')
    readonly_fields = ('user',)
    search_fields = ['user__username']
    def get_username(self, i):
        return i.user.username

class HoursInline(admin.TabularInline):
    model = WorkTimer
    fields = ('value', 'token')
    readonly_fields = ('token',)
    extra = 0

@admin.register(TimeSheet)
class BillableHoursAdmin(admin.ModelAdmin):
    fields = ('username',)
    readonly_fields = ('username', 'billable_hours',)
    list_display = ('username', 'get_billable_hours')

    inlines = [
        HoursInline
    ]

    def billable_hours(self, x):
        return x.get_billable_hours()

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0

    readonly_fields = ('timestarted', 'timefinished',)

@admin.register(MenuEntry)
class MenuEntryAdmin(admin.ModelAdmin):

    readonly_fields = ('user', 'menu',)

    inlines = [
        MenuItemInline
    ]
