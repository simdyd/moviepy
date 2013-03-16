from download.download_serietv import *
from serietv.models import *



supporti=Supporti.objects.all()
for supporto in supporti:
    supporto.link_episodi()
    supporto.save()

