from django.contrib import admin
from .models import WorkTimer, Task, EventLog
from django.contrib.auth.models import User
import user_patch
# Register your models here.

class TimeSheet(User):
    class Meta:
       proxy = True

@admin.register(WorkTimer)
class WorkTimerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'token', 'value', 'timestamp',)
    readonly_fields = ('user','timestamp')
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

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    readonly_fields = ('user', 'image',)
    search_fields = ['user__username']
@admin.register(EventLog)
class EventLog(admin.ModelAdmin):
    list_display = ('get_username', 'name', 'timestamp',)

    def get_username(self, x):
        return x.task.user.username
