from download.download_serietv_coming import *
from serietv.models import *
from link.models import *
from django.contrib.contenttypes.models import ContentType

#Popolo tabella dei link
#for serie in Serietv.objects.all():
#    try:
#        link=Link.objects.get(tipo='sharetv',content_object=serie)
#    except:
#        link=Link(content_object=serie, tipo='sharetv')
#    link.link=serie.link
#    link.save()
content_type=ContentType.objects.get_for_model(Serietv)

for link in Link.objects.filter(content_type=content_type,tipo='comingsoon'):
    #print link
    #oggetto=link.content_object
    serietv=Serietv.objects.get(id=link.object_id)
    download_serie_detail(link,serietv)
    link_episodi=link.link.replace('/Scheda/','/Scheda/Episodi/')

    download_stagioni(serietv,link_episodi)
    print link_episodi

#
#res=trova_serie('kyle xy')
#count=0
#for serie in res:
#    print serie.titolo
#
#
#    try:
#        serietv=Serietv.objects.get(nome=serie.titolo)
#    except:
#        serietv=Serietv()
#        serietv.nome=serie.titolo
#        serietv.link=serie.link
#        serietv.save()
#    download_stagioni(serie,serietv)
#    count=count+1
#
#