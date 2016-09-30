import website.wsgi
from data.models import Treatment


for t in Treatment.objects.filter(batch="2"):
    if int(t.frameorder[0]) == 1:
        t.frameorder = 121212121212
    elif int(t.frameorder[0]) == 2:
        t.frameorder = 212121212121
    else:
        print "No change"
    t.save()

