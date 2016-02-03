from django.core.management.base import BaseCommand, CommandError
from data.models import Task, Image
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Assigns all users a task relating to an image"

    def handle(self, *args, **options):
        for user in User.objects.all():
            for image in Image.objects.all():
                task, created = Task.objects.get_or_create(user_id=user.id, image_id=image.id)

