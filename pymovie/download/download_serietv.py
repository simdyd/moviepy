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

path_base=settings.PATH_BASE
site_base='http://sharetv.org'

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
   

def download_episodi(stagione,serietv):
    urllib.urlretrieve(stagione.link,path_base+'tmp/download_episodi.html')
    input=open(path_base+'tmp/download_episodi.html')
    pagina=input.read()
    
    stringa='<table width=750 class="res"'
    pos=pagina.find(stringa)
    pos2=pagina.find('</table>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    #print tmp
    
    pos=tmp.find('<u>')
    while pos>0:
        pos2=tmp.find('</u>',pos+3)
        test=tmp[pos+3:pos2]
        if test.find('x'):
            num_stagione=test[:test.find('x')]
            num_episodio=test[test.find('x')+1:test.find(' ')]
            titolo_episodio=test[test.find(' ')+1:]
              
            pos_=tmp.find('<br>',pos2)
            pos_2=tmp.find('</td>',pos_+4)
            trama=tmp[pos_+4:pos_2]
            
            #data
            pos_=tmp.find('>',pos_2+5)
            pos_2=tmp.find('<',pos_+1)
            data=tmp[pos_+1:pos_2]
            
            #ricavo il link
            pos_3=tmp.rfind('href="',0,pos)
            if pos_3>-1:
                pos_2=tmp.find('"',pos_3+6)
                link_episodio=site_base+tmp[pos_3+6:pos_2]
                #print link_episodio
            else:
                link_episodio=''
            
            #ricavo il link foto
            pos_3=tmp.rfind('<img src="',0,pos)
            if pos_3>-1:
                pos_2=tmp.find('"',pos_3+10)
                link_foto=site_base+tmp[pos_3+10:pos_2]
                #print link_foto
            else:
                link_foto=''
            
            try:
                episodio=Episodi.objects.get(serietv=serietv,stagione=num_stagione,episodio=num_episodio)
            except:
                episodio=Episodi()
                episodio.serietv=serietv
                episodio.stagione=num_stagione
                episodio.episodio=num_episodio
                episodio.titolo=titolo_episodio
                episodio.link=link_episodio
                episodio.trama=trama
                episodio.data=data
                episodio.visto=0
                episodio.save()
            if link_foto!='':
                download_foto_episodio(episodio,link_foto)
        pos=tmp.find('<u>',pos2)
        #<u>1x01 Pilot</u>
        
def download_stagioni(serie,serietv):
    urllib.urlretrieve(serie.link,path_base+'tmp/download_stagioni.html')
    input=open(path_base+'tmp/download_stagioni.html')
    pagina=input.read()
    
    stringa='<h2>Season Guides</h2>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</ul>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    #print tmp
    
    stringa="<a href='"
    pos=tmp.find(stringa)
    while pos>0:
        stagione=stagioni_model()
        
        pos2=tmp.find("'",pos+len(stringa))
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
            pass
    
def trova_serie(titolo):
    titolo=titolo.replace(' ','+')
    urllib.urlretrieve('http://sharetv.org/search/'+titolo+'/',path_base+'tmp/trova_serie.html')
    input=open(path_base+'tmp/trova_serie.html')
    pagina=input.read()
    stringa='<table width=700 border=0 cellpadding=4 cellspacing=0 class="res">'
    pos=pagina.find(stringa)
    pos2=pagina.find('</table>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    res=[]
    stringa='<a href="'
    pos=tmp.find(stringa)
    while pos>0:
        pos2=tmp.find('"',pos+len(stringa))
        link=tmp[pos+len(stringa):pos2]
        pos_=tmp.find('>',pos2)
        pos_2=tmp.find('</a>',pos_+1)
        titolo=tmp[pos_+1:pos_2]
        check=titolo.find('<')
        #print check
        if check==-1:
            serie=serie_model()
            serie.link=site_base+link
            serie.titolo=titolo
            res.append(serie)
        pos=tmp.find(stringa,pos2)
    #print tmp
    
    return res