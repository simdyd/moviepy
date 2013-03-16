import urllib, urllister
from django.db import models
from django.conf import settings


path_base=settings.PATH_BASE
site_base='http://www.imdb.it/'

def get_info_imdb(link,link_type=1):
    if link_type==1:
        link=site_base+link
    urllib.urlretrieve(link,path_base+'tmp/file_info_imdb.html')
    input=open(path_base+'tmp/file_info_imdb.html')
    result={}
    persone={}
    count_persone=0
    
    
    return result,persone

def trova_titoli_imdb(titolo,link_type=1):
    titolo=titolo.replace(' ','+')
    
    urllib.urlretrieve("http://www.imdb.it/find?s=all&q"+titolo,path_base+'tmp/file_imdb.html')
    input=open(path_base+'tmp/file_imdb.html')
    pagina=input.read()

    #Ricavo la parte interessante nella ricerca
    pos=pagina.find('<p><b>Titoli popolari</b>')
    pos2=pagina.find(chr(13)+chr(10),pos)
    risultati=pagina[pos:pos2]
    print risultati
    tmp=risultati
    count=0
    res=[]
   
    while (count<10):
        pos=tmp.find('<a class="title"')
        #print 'pos' + str(pos)
        if pos>0:
            titolo=titoli_model()
            #ricavo il collegamento
            pos=tmp.find('href="',pos)
            pos2=tmp.find('"',pos+6)
            #print str(count) + ' ' + str(pos) + ' ' + str(pos2)
            #print tmp[pos+6:pos2]
            titolo.link=tmp[pos+6:pos2]
            if link_type==1:
                titolo.link=titolo.link.replace(site_base,'')
            #ricavo il titolo
            pos=tmp.find('title="',pos2)
            pos2=tmp.find('"',pos+7)
            #print tmp[pos+7:pos2]
            titolo.titolo=tmp[pos+7:pos2]
            pos2=tmp.find('</a>',pos)
        
            #print str(count) + ' ' + str(pos) + ' ' + str(pos2)
            #
            stringa="<li>Uscita: <span>"
            pos=tmp.find(stringa,pos2)
            pos2=tmp.find("</span>",pos+len(stringa))
            titolo.anno=tmp[pos+len(stringa):pos2]
            tmp=tmp[pos2:]
            res.append(titolo)
        count=count+1
    
    return res