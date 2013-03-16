from download.download_serietv import *
from serietv.models import *
from link.models import *


#Popolo tabella dei link
#for serie in Serietv.objects.all():
#    try:
#        link=Link.objects.get(tipo='sharetv',content_object=serie)
#    except:
#        link=Link(content_object=serie, tipo='sharetv')
#    link.link=serie.link
#    link.save()

#for episodio in Episodi.objects.all():
#    if episodio.link!=None:
#        try:
#            link=Link.objects.get(tipo='sharetv',content_object=episodio)
#        except:
#            link=Link(content_object=episodio, tipo='sharetv')
#        link.link=episodio.link
#        link.save()

#
res=trova_serie('merlin')
count=0
for serie in res:
    print serie.titolo


    try:
        serietv=Serietv.objects.get(nome=serie.titolo)
    except:
        serietv=Serietv()
        serietv.nome=serie.titolo
        serietv.link=serie.link
        serietv.save()

    try:
        link=Link.objects.get(tipo='sharetv',content_object=serietv)
    except:
        link=Link(content_object=serietv, tipo='sharetv')
    link.link=serie.link
    link.download=False
    link.save()

    download_stagioni(serie,serietv)
    count=count+1
#
#