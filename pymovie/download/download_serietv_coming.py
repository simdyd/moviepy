import urllib, urllister
from django.db import models
from django.conf import settings
from serietv.models import *
import datetime
import os
import sys
import Image
from media.models import Photo
#from film.models import *
#usock = urllib.urlopen("http://www.35mm.it/search/?string=ember&year=0&month=0&day=0&sections[]=film&open_tab=0/")
from link.models import Link

path_base=settings.PATH_BASE
site_base='http://www.comingsoon.it'

class serie_model():
    id = models.AutoField(primary_key=True)
    titolo = models.TextField()
    link = models.TextField()

class stagioni_model():
    id = models.AutoField(primary_key=True)
    titolo = models.TextField()
    link = models.TextField()


def download_foto_episodio(episodio,link_foto):
    count=0
    ok=True
    now=datetime.datetime.now()
    new_file_dir = os.path.dirname(settings.MEDIA_ROOT+now.strftime("%Y"+os.sep+"%m"+os.sep))
    if not os.path.exists(new_file_dir):
        os.makedirs(new_file_dir)

    try:
        link=link_foto
        pos=link.rfind('/')
        nome_foto=link[pos+1:]
        if nome_foto.find('no_image')==-1:
            try:
                nome_foto=nome_foto.replace('%20','_')
                name = now.strftime("%Y"+os.sep+"%m"+os.sep) + 'ep_' + str(episodio.id) + nome_foto
                image = urllib.URLopener()
                image.retrieve(link,settings.MEDIA_ROOT + name)

                try:
                    img = Photo.objects.get(image=name)
                except:
                    img = Photo()
                    img.name = nome_foto
                    img.image=name
                    img.caption=episodio.titolo
                    img.upload_date = datetime.datetime.now()
                    img.publish_date = datetime.datetime.now()

                    img.save()

                    episodio.foto.add(img)
                    episodio.save()
            except:
                print sys.exc_info()[0]
                print nome_foto
                print 'problemi con download foto'

    except:
        ok=False


def download_dettagli_episodio(episodio):
    print 'AAAAAAA'
    link=Link.objects.get(tipo='comingsoon',content_object=episodio)
    print site_base+link.link
    urllib.urlretrieve(site_base+link.link,path_base+'tmp/download_episodio_detail_coming.html')
    input=open(path_base+'tmp/download_episodio_detail_coming.html')


    input.close()

def download_episodi(stagione,serietv):
    urllib.urlretrieve(stagione.link,path_base+'tmp/download_episodi_coming.html')
    input=open(path_base+'tmp/download_episodi_coming.html')
    pagina=input.read()
    input.close()
    stringa='<h1 class="titoloFilm">'
    pos=pagina.find(stringa)
    pos2=pagina.find('</table>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    #print tmp
    stringa2="<div class='rowStgEpsList'>"
    pos=tmp.find(stringa2)
    #<a href="/SerieTV/Scheda/Episodi/?key=24&amp;stg=1&amp;eps=1" class="titoloFilm">1.01 Genesi</a><br>(In His Own Image)')
    while pos>0:
        pos2=tmp.find('</div>',pos+len(stringa2))

        test=tmp[pos+len(stringa2):pos2]
        #print test
        if test.find('stg='):
            pos3=test.find('stg=')
            pos4=test.find('&',pos3)
            num_stagione=test[pos3+len('stg='):pos4]
        else:
            num_stagione=None
        if test.find('eps'):
            pos3=test.find('eps=')
            pos4=test.find("'",pos3)
            num_episodio=test[pos3+len('eps='):pos4]
        else:
            num_episidio=None


        #print num_stagione
        #print num_episodio
        if num_stagione!=None and num_episodio!=None:
            #titolo
            pos3=test.find('>')
            pos4=test.find('<',pos3)
            titolo=test[pos3+1:pos4]
            pos3=titolo.find(' ')
            titolo=titolo[pos3+1:]
            #print titolo

            #link
            pos3=test.find("href='")
            pos4=test.find("'",pos3+6)
            link_ep=test[pos3+6:pos4]
            #print link

            #titolo originale
            pos3=test.find("<br />(")
            pos4=test.find(")",pos3+7)
            titolo_ori=test[pos3+7:pos4]
            #print titolo_ori

            try:
                episodio=Episodi.objects.get(serietv=serietv,stagione=num_stagione,episodio=num_episodio)
            except:
                episodio=Episodi()
                episodio.serietv=serietv
                episodio.stagione=num_stagione
                episodio.episodio=num_episodio

                #episodio.link=link_episodio
                #episodio.trama=trama
                #episodio.data=data
                episodio.visto=0
            episodio.titolo=titolo
            episodio.save()

            try:
                link=Link.objects.get(tipo='comingsoon',content_object=episodio)
            except:
                link=Link(content_object=episodio, tipo='comingsoon')
                link.download=False

            link.link=link_ep
            link.save()
            #print link_ep
            download_dettagli_episodio(episodio)
        pos=tmp.find(stringa2,pos2)


def download_serie_detail(link,serietv):

    urllib.urlretrieve(link.link,path_base+'tmp/detail_serie_coming.html')
    input=open(path_base+'tmp/detail_serie_coming.html')
    pagina=input.read()
    stringa='<div id="schedaFilm">'
    pos=pagina.find(stringa)
    pos2=pagina.find("<br clear='all'>",pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    #print tmp
    if pos>0:
        #estraggo il titolo
        stringa="<h1 class='titoloFilm'>"
        pos=tmp.find(stringa)
        pos2=tmp.find('</h1>',pos+len(stringa))
        titolo=tmp[pos+len(stringa):pos2]
        #print titolo
        serietv.titolo=titolo
        #titolo originale

        stringa="<h2 class='titoloFilm2'>"
        pos=tmp.find(stringa)
        pos2=tmp.find('</h2>',pos+len(stringa))
        titolo_originale=tmp[pos+len(stringa):pos2].replace('(','').replace(')','')

        serietv.titolo_originale=titolo_originale

        stringa='<div class="invertedshiftdown">'
        pos=tmp.find(stringa)
        pos2=tmp.find('</div>',pos+len(stringa))
        tmp2=tmp[pos+len(stringa):pos2]

        stringa='<a href="'
        pos=tmp2.find(stringa)

        link_episodi=None
        link_cast=None
        link_foto=None

        while pos>0:
            pos2=tmp2.find('"',pos+len(stringa))
            link_=tmp2[pos+len(stringa):pos2]

            pos3=link_.find('/Cast/')
            if pos3>0:
                link_cast=link_
            pos3=link_.find('/Episodi/')
            if pos3>0:
                link_episodi=link_
            pos3=link_.find('/Foto/')
            if pos3>0:
                link_foto=link_
            tmp2=tmp2[pos2:]
            pos=tmp2.find(stringa)
        #print link_cast
        #print link_episodi
        #print link_foto

        #trama
        stringa="<span class='vociFilm'>Trama: </span>"
        pos=tmp.find(stringa)
        pos2=tmp.find('</div>',pos+len(stringa))
        trama=tmp[pos+len(stringa):pos2]
        serietv.trama=trama.decode('iso-8859-1','replace')
        #paese
        stringa="<span class='vociFilm'>PAESE: </span>"
        pos=tmp.find(stringa)
        pos2=tmp.find('<br />',pos+len(stringa))
        paese=tmp[pos+len(stringa):pos2]
        serietv.paese=paese

        #produzione
        stringa="<span class='vociFilm'>PRODUZIONE: </span>"
        pos=tmp.find(stringa)
        pos2=tmp.find('<br />',pos+len(stringa))
        produzione=tmp[pos+len(stringa):pos2]
        serietv.produzione=produzione

        #genere
        stringa="<span class='vociFilm'>GENERE: </span>"
        pos=tmp.find(stringa)
        pos2=tmp.find('<br />',pos+len(stringa))
        genere=tmp[pos+len(stringa):pos2]
        serietv.genere=genere

        stringa="<span class='vociFilm'>DURATA: </span>"
        pos=tmp.find(stringa)
        pos2=tmp.find('<br />',pos+len(stringa))
        durata=tmp[pos+len(stringa):pos2]
        serietv.durata=durata
        try:
            serietv.save()
        except:
            pass
    input.close()

def download_stagioni(serietv,link):

    urllib.urlretrieve(link,path_base+'tmp/download_stagioni_comingsoon.html')
    input=open(path_base+'tmp/download_stagioni_comingsoon.html')
    pagina=input.read()

    stringa='<p class="red">STAGIONI: </p>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    #print tmp

    stringa='<a href="'
    pos=tmp.find(stringa)
    while pos>0:
        stagione=stagioni_model()

        pos2=tmp.find('"',pos+len(stringa))
        link=tmp[pos+len(stringa):pos2]
        #print link
        stagione.link=site_base+link
        pos_=tmp.find('>',pos2)
        pos_2=tmp.find('</a>',pos_)
        nome=tmp[pos_+1:pos_2]
        #print nome
        stagione.titolo=nome
        pos=tmp.find(stringa,pos2)
        try:
            download_episodi(stagione,serietv)
        except:
            print sys.exc_info()