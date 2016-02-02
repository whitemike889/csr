from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def get_now():
    return timezone.now()
# Create your models here.

class Image(models.Model):
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
        return self.get_url()

class WorkTimer(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField()
    token = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    LIKERT = (
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neither Agree or Disagree"),
        (4, "Agree"),
        (5, "Stronly Agree"),
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

    YEARS = [(x,x) for x in range(2000, timezone.now().year+1)]

    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    address = models.CharField('Street Address', max_length=768)
    finished = models.IntegerField(choices=CHOICES, default=0)
    month = models.IntegerField(choices=MONTHS)
    year = models.IntegerField(choices=YEARS)
    pic_quality = models.IntegerField("Picture Quality", choices=LIKERT)
    str_quality = models.IntegerField("Street Quality", choices=LIKERT)
    pot_holes = models.IntegerField("Pot Holes", choices=NUMBERS)
    bui_quality = models.IntegerField("Building Quality", choices=LIKERT)
    car_quality = models.IntegerField("Car Quality", choices=LIKERT)
    litter = models.IntegerField(choices=LIKERT)
    road_work = models.IntegerField("Road Work", choices=CHOICES)
    for_sale = models.IntegerField("Houses for sale signs", choices=CHOICES)
    shoes = models.IntegerField("Shoes on wire", choices=CHOICES)
    people = models.IntegerField("People actively covering faces", choices=CHOICES)
    broken_signs = models.IntegerField("Broken Street Signs", choices=CHOICES)
    trees = models.IntegerField(choices=CHOICES)

    timestarted = models.DateTimeField(default=get_now)
    timefinished = models.DateTimeField(null=True, blank=True)

    ## WRITE A VIEW TO OVERRIDE SAVE FUNCTION THAT CHECKS IF FINISHED IS MARKED!
    def save(self, *args, **kwargs):
        if self.finished == 1 and self.timefinished == None:
            self.timefinished = get_now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.restaurantName or "Blank"

def get_now():
    return timezone.now()

class EventLog(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(default=get_now)



