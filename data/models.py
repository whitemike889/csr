from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def get_now():
    return timezone.now()
# Create your models here.

class Menu(models.Model):
    filename = models.CharField('Filename', max_length=512)

    def get_url(self):
        return "http://bfidata.s3-website-us-east-1.amazonaws.com/menus/{}".format(self.filename)

    def check_status(self,user):
        rs = user.menuentry_set.filter(menu_id=self.id)
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

class MenuEntry(models.Model):
    CHOICES = (
        (0, "No"),
        (1, "Yes"),
    )

    user = models.ForeignKey(User)
    menu = models.ForeignKey(Menu)
    restaurantName = models.CharField('Restaurant Name', max_length=512)
    finished = models.IntegerField(choices=CHOICES, default=0)
    timestarted = models.DateTimeField(default=get_now)
    timefinished = models.DateTimeField(null=True, blank=True)

    ## WRITE A VIEW TO OVERRIDE SAVE FUNCTION THAT CHECKS IF FINISHED IS MARKED!
    def save(self, *args, **kwargs):
        if self.finished == 1 and self.timefinished == None:
            self.timefinished = get_now()
        super(MenuEntry, self).save(*args, **kwargs)

    def __str__(self):
        return self.restaurantName or "Blank"


class MenuItem(models.Model):
    CHOICES = (
        ('S', "Side/App"),
        ('B', "Beverage"),
        ('E', "Entree"),
    )
    menuentry = models.ForeignKey(MenuEntry)
    name = models.CharField("Item Name", max_length=512, blank=True)
    price = models.CharField("Price", max_length=256, blank=True)
    classification = models.CharField(max_length=2, choices=CHOICES)
    timestarted = models.DateTimeField(default=get_now)
    timefinished = models.DateTimeField(auto_now_add=True)


def get_now():
    return timezone.now()

class EventLog(models.Model):
    menuentry = models.ForeignKey(MenuEntry)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(default=get_now)



