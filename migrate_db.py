
import website.wsgi
from django.conf import settings


from data.models import Menu

localMenus = Menu.objects.using('local').all()

for m in localMenus:
    remoteMenus, created = Menu.objects.using('default').get_or_create(filename=m.filename)

