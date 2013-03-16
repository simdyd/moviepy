import urllib, urllister
from django.db import models
from django.conf import settings

path_base=settings.PATH_BASE
site_base='http://www.film.tv.it/'


def get_info_filmtv(link,link_type=1):
    if link_type==1:
        link=site_base+link
    
    link=link.replace('\\','/')
    print link
    urllib.urlretrieve(link,path_base+'tmp/file_info_filmtv.html')
    input=open(path_base+'tmp/file_info_filmtv.html')
    pagina=input.read()
    result={}
    foto_link={}
    
    result['link']=link
    ##Recupero titolo FILM
    pos=pagina.find('<h1>')
    if pos>0:
        pos2=pagina.find('</h1>',pos)
        result['titolo']=pagina[pos+len('<h1>'):pos2]
        print result['titolo']
        result['titolo_originale']=''
        
    ##Recupero trama
    stringa='<p class="trama">'
    pos=pagina.find(stringa)
    if pos>0:
        pos2=pagina.find('</p>',pos)
        result['descrizione']=pagina[pos+len(stringa):pos2]
        print result['descrizione']
    else:
        result['descrizione']=''
    
    ##Recupero dati film
    pos=pagina.find('<div id="filmDati">')
    print 'pos ' + str(pos) 
    if pos>0:
        pos2=pagina.find('</div>',pos)
        blocco=pagina[pos:pos2]
        
        ##Ricavo Nazione
        stringa="nazione="
        pos=blocco.find(stringa)
        
        pos2=blocco.find('"',pos)
        result['nazione']=blocco[pos+len(stringa):pos2]
        print result['nazione']
        
        ##Ricavo anno
        stringa="anno="
        pos=blocco.find(stringa)
        
        pos2=blocco.find('"',pos)
        result['anno']=blocco[pos+len(stringa):pos2]
        print result['anno']
        
        ##Genere
        stringa="genere="
        pos=blocco.find(stringa)
        pos=blocco.find('>',pos)
        pos2=blocco.find('</a>',pos)
        result['genere']=blocco[pos+1:pos2]
        print result['genere']
        
        ##Durata
        stringa=", durata "
        pos=blocco.find(stringa)
        if pos>0:
            pos2=blocco.find(']',pos)
            result['durata']=blocco[pos+len(stringa):pos2]
        else:
            result['durata']='0'
        print result['durata']
        
    return result,foto_link

class titoli_model():
    id = models.AutoField(primary_key=True)
    titolo = models.TextField()
    link = models.TextField()
    anno = models.TextField()
    note = models.TextField()
    
def trova_titoli_filmtv(titolo,link_type=1):
    titolo=titolo.replace(' ','+')
    
    urllib.urlretrieve("http://www.film.tv.it/cerca.php?q="+titolo,path_base+'tmp/lista_filmtv.html')
    input=open(path_base+'tmp/lista_filmtv.html')
    
    pagina=input.read()

    #Ricavo la parte interessante nella ricerca
    pos=pagina.find('<!--film-->')
    pos2=pagina.find('<!-- fine ricerca -->')
    risultati=pagina[pos:pos2]

    tmp=risultati
    count=0
    res=[]
   
    while (count<50):
        pos=tmp.find('<dt><h3><a')
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
            titolo.link=titolo.link.replace('/','\\')
            #ricavo il titolo
            pos=tmp.find('title="',pos2)
            pos2=tmp.find('"',pos+7)
            #print tmp[pos+7:pos2]
            titolo.titolo=tmp[pos+7:pos2]
            pos2=tmp.find('</a>',pos)
        
            #print str(count) + ' ' + str(pos) + ' ' + str(pos2)
            #
            stringa="("
            pos=tmp.find(stringa,pos2)
            pos2=tmp.find(")",pos+len(stringa))
            titolo.anno=tmp[pos+len(stringa):pos2]
            #titolo.anno=''
            tmp=tmp[pos2:]
            res.append(titolo)
        count=count+1
    
    return res