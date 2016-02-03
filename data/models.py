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
    finished = models.IntegerField(choices=CHOICES, default=0)


    street = models.CharField('Street Address', max_length=768, null=True)
    citystate = models.CharField("City, State", max_length=512, null=True)
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
            "The quality of the cars visible in the picture is high",
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
    for_sale = models.IntegerField(
            "There are one more house for sale signs visible in the picture",
            choices=CHOICES, null=True
    )
    shoes = models.IntegerField(
            "Are there shoes on a wire visible in the picture",
            choices=CHOICES, null=True
    )
    people = models.IntegerField(
            "Are there people actively covering their faces visible in the picture",
            choices=CHOICES, null=True
    )
    broken_signs = models.IntegerField(
            "Are there any broken street signs visible in the picture",
            choices=CHOICES, null=True
    )
    trees = models.IntegerField(
            "Are there trees visible in the picture",
            choices=CHOICES, null=True
    )

    timestarted = models.DateTimeField(default=get_now)
    timefinished = models.DateTimeField(null=True, blank=True)

    ## WRITE A VIEW TO OVERRIDE SAVE FUNCTION THAT CHECKS IF FINISHED IS MARKED!
    def save(self, *args, **kwargs):
        if self.finished == 1 and self.timefinished == None:
            self.timefinished = get_now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.street or self.image.filename

def get_now():
    return timezone.now()

class EventLog(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(default=get_now)



