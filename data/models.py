from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

def get_now():
    return timezone.now()
# Create your models here.

class Constants:
    workdates = {
        '1': {
            'start': datetime.datetime(2016, 5, 10, 0, 01),
            'end': datetime.datetime(2016, 5, 13, 23, 59),
            }
        }
class Treatment(models.Model):
    user = models.OneToOneField(User)
    wage = models.CharField("Wage Rate", max_length=128)
    tutorial = models.IntegerField(default=0)
    timezone = models.CharField(max_length=128, null=True)
    batch = models.CharField(max_length=64, null=True)
    #login or day
    assignment = models.CharField(max_length=64, null=True)
    frameorder = models.CharField(max_length=64, null=True)

    def get_access(self):
        start = Constants.workdates[self.batch]['start']
        end = Constants.worksdates[self.batch]['end']

        start = timezone.make_aware(start, self.timezone)
        end = timezone.make_aware(start, self.timezone)
        today = timezone.make_aware(datetime.datetime.now(), self.timezone)
        if today > start and today < end:
            access = True
        else:
            access = False

        return dict(access=access, start=start, end=end, today=today)

    def get_frame(self):
        access = self.get_access()
        if not access['access']:
            return False
        if self.assignment == 'day':
            day = access['today'] - access['start']
            day = int(day.days)
        if self.assigment == 'login':
            logins = EventLog.objects.filter(user=self.user_id, name='login')
            day = 0
            for x in range(1,len(logins)):
                curr = timezone.make_aware(login[x], self.timezone)
                prev = timezone.make_aware(login[x-1], self.timezone)
                if curr.date() != prev.date():
                    day += 1
        frame = self.frameorder[day]

class Image(models.Model):
    order = models.IntegerField()
    filename = models.CharField('Filename', max_length=512)

    def get_url(self):
        return "http://bfidata.s3-website-us-east-1.amazonaws.com/streetviews/{}".format(self.filename)

    def check_status(self,user):
        rs = user.task_set.filter(task_id=self.id)
        if rs.count() == 1:
            status = rs[0].finished
        else:
            status = 0
        return status

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['order']

class WorkTimer(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey("Task", null=True)
    page = models.CharField(max_length=28, null=True)
    value = models.IntegerField()
    token = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    LIKERT = (
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neither Agree or Disagree"),
        (4, "Agree"),
        (5, "Strongly Agree"),
        (6, "N/A"),
    )

    NUMBERS = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "5+"),
        (7, "N/A"),
    )

    CHOICES = (
        (0, "No"),
        (1, "Yes"),
        (2, "N/A"),
    )

    MONTHS = (
        (1, "Jan"),
        (2, "Feb"),
        (3, "Mar"),
        (4, "Apr"),
        (5, "May"),
        (6, "Jun"),
        (7, "Jul"),
        (8, "Aug"),
        (9, "Sep"),
        (10, "Oct"),
        (11, "Nov"),
        (12, "Dec"),
    )

    states = [
        "AL", "AK", "AZ", "AR", "CA",
        "CO", "CT", "DC", "DE", "FL",
        "GA", "HI", "ID", "IL", "IN",
        "IA", "KS", "KY", "LA", "ME",
        "MD", "MA", "MI", "MN", "MS",
        "MO", "MT", "NE", "NV", "NH",
        "NJ", "NM", "NY", "NC", "ND",
        "OH", "OK", "OR", "PA", "RI",
        "SC", "SD", "TN", "TX", "UT",
        "VT", "VA", "WA", "WV", "WI",
        "WY",
    ]
    states2 = []
    for state in states:
        states2.append((state, state))


    YEARS = [(x,x) for x in range(2000, timezone.now().year+1)]

    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    finished = models.IntegerField(choices=CHOICES, default=0)


    street_num = models.CharField('Street #', max_length=64, null=True)
    street_nam = models.CharField('Street name', max_length=512, null=True)
    city = models.CharField("City", max_length=512, null=True)
    state = models.CharField("State", choices=states2, max_length=4, null=True)
    month = models.IntegerField(choices=MONTHS, null=True)
    year = models.IntegerField(choices=YEARS, null=True)
    pic_quality = models.IntegerField(
            "The quality of the actual picture is high",
            choices=LIKERT, null=True
    )
    str_quality = models.IntegerField(
            "The quality of the streets visible in the picture is high",
            choices=LIKERT, null=True
    )
    pot_holes = models.IntegerField(
            "How many potholes are visible in the picture",
            choices=NUMBERS, null=True
    )
    bui_quality = models.IntegerField(
            "The quality of buildings visible in the picture is high",
            choices=LIKERT, null=True
    )
    car_quality = models.IntegerField(
            "The quality of the vehicles visible in the picture is high",
            choices=LIKERT, null=True
    )
    litter = models.IntegerField(
            "The amount of litter visible in the picture is high",
            choices=LIKERT, null=True
    )
    road_work = models.IntegerField(
            "Are there signs of road work visible in the picture",
            choices=CHOICES, null=True
    )
    graffiti = models.IntegerField(
            "Is there graffiti visible in the picture",
            choices=CHOICES, null=True
    )
    for_sale = models.IntegerField(
            "There are one or more house for sale signs visible in the picture",
            choices=CHOICES, null=True
    )
    shoes = models.IntegerField(
            "Are there shoes on a wire visible in the picture",
            choices=CHOICES, null=True
    )
    trees = models.IntegerField(
            "Are there trees and/or large bushes visible in the picture",
            choices=CHOICES, null=True
    )
    broken_signs = models.IntegerField(
            "Are there any broken street signs visible in the picture",
            choices=CHOICES, null=True
    )
    people = models.IntegerField(
            "Are there people actively covering their faces visible in the picture",
            choices=CHOICES, null=True
    )

    timestarted = models.DateTimeField(default=get_now)
    timefinished = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.finished == 1 and self.timefinished == None:
            self.timefinished = get_now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        if self.street_num and self.street_nam:
            y = "{}".format(self.year) if self.year else ""
            m = self.month if self.month else ""
            return "{} {} {}-{}".format(self.street_num, self.street_nam, m, y)
        else:
            return self.image.filename


def get_now():
    return timezone.now()

class EventLog(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task, null=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(default=get_now)

    class Meta:
        ordering = ['timestamp']

