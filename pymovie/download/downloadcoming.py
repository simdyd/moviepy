import urllib, urllister
from django.db import models
from django.conf import settings

site_base='http://www.comingsoon.it/'
path_base=settings.PATH_BASE

def get_info_comingsoon(link,link_type=1):
    link=str(link).replace('&&','?')
    link=str(link).replace('|','/')
    if link_type==1:
        link=site_base+link
    #print 'link' + link
    urllib.urlretrieve(link,path_base+'tmp/file_info_comingsoon.html')
    input=open(path_base+'tmp/file_info_comingsoon.html')
    result={}
    persone={}
    foto_link={}
    count_persone=0
    result['link']=link
    pagina=input.read()
    pos=pagina.find('<div id="schedaFilm">')
    pagina=pagina[pos:]
    #Titolo<h1 class='titoloFilm'>La bussola d'oro</h1>
    pos=pagina.find("<h1 class='titoloFilm'>")
    pos2=pagina.find('</h1>',pos+23)
    result['titolo']=pagina[pos+23:pos2].strip()
    #print result['titolo']
    
    
    #Titolo originale 
    result['titolo_originale']=None
    #print result['titolo_originale']
    #print pagina
    
    #Trova link locandina
    stringa='title="locandina'
    pos=pagina.find(stringa)
    tmp=pagina[0:pos]
    pos2=tmp.rfind('<a href="')
    pos3=tmp.find('"',pos2+9)
    tmp=tmp[pos2+9:pos3].strip()
    foto_link[0]=tmp
    #print foto_link[0]
    
    #Trama 
    stringa="<span class='vociFilm'>Trama del film"
    pos=pagina.find(stringa)
    pos=pagina.find("<br />",pos)
    pos2=pagina.find("<br />",pos+6)
    result['descrizione']=pagina[pos+6:pos2]
    #print result['descrizione']
    
    #Genere
    stringa="<span class='vociFilm'>GENERE: </span>"
    pos=pagina.find(stringa)
    pos2=pagina.find("<br />",pos+len(stringa))
    result['genere']=pagina[pos+len(stringa):pos2]
    
    #durata
    stringa="<span class='vociFilm'>DURATA: </span>"
    pos=pagina.find(stringa)
    pos2=pagina.find("<br />",pos+len(stringa))
    result['durata']=pagina[pos+len(stringa):pos2]
    
    #Nazione
    
    stringa="<span class='vociFilm'>PAESE: </span>"
    pos=pagina.find(stringa)
    pos2=pagina.find("<br />",pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    pos=tmp.rfind(' ')
    result['anno']=tmp[pos:].strip()
    result['nazione']=tmp[:pos].strip()
    
    
    result['link']=link
    #ricerco gli attori...
    
    stringa="<span class='vociFilm'>ATTORI: </span>"
    pos=pagina.find(stringa)
    pos2=pagina.find("<div",pos+len(stringa))
    tmp=pagina[pos:pos2]
    pos=tmp.find('<a href="')
    count_persone=0
    while (pos>0):
        pos=tmp.find('>',pos)
        pos2=tmp.find('<',pos)
        attore=tmp[pos+1:pos2]
        #print attore
        if attore!='</a>':
            persone[count_persone,'nome']=attore
            persone[count_persone,'professione']='ATT'
            count_persone=count_persone+1
        tmp=tmp[pos2:]
        
        pos=tmp.find('<a href="')
    
    stringa="<span class='vociFilm'>REGIA: </span>"
    pos=pagina.find(stringa)
    pos2=pagina.find("<br />",pos+len(stringa))
    tmp=pagina[pos:pos2]
    pos=tmp.find('<a href="')
    
    while (pos>0):
        pos=tmp.find('>',pos)
        pos2=tmp.find('<',pos)
        regista=tmp[pos+1:pos2]
        #print attore
        if regista!='</a>':
            persone[count_persone,'nome']=regista
            persone[count_persone,'professione']='REG'
            count_persone=count_persone+1
        tmp=tmp[pos2:]
        
        pos=tmp.find('<a href="')
      
    #1print tmp
    
    return result,persone,foto_link
    

class titoli_model():
    id = models.AutoField(primary_key=True)
    titolo = models.TextField()
    link = models.TextField()
    anno = models.TextField()
    note = models.TextField()
    
    


def trova_titoli_comingsoon(titolo,link_type=1):
    titolo=titolo.replace(' ','%20')
    
    #http://www.comingsoon.it/Film/Database/?titoloFilm=preghiera%20maledetta
    url="http://www.comingsoon.it/Film/Database/?titoloFilm="+titolo
    urllib.urlretrieve(url,path_base+'tmp/filecomingsoon.html')
    
    #print url
    
    input=open(path_base+'tmp/filecomingsoon.html')
    pagina=input.read()

    #Ricavo la parte interessante nella ricerca
    #pos=pagina.find('<div id="divisione"></div>')
    #pos2=pagina.find('<div id="bottombox"></div>')
    #risultati=pagina[pos:pos2]
    #print pos
    #print pos2
    tmp=pagina
    count=0
    res=[]
   
    while (count<10):
        pos=tmp.find('<div id="BoxFilm">')
        tmp=tmp[pos:]
        #print 'pos' + str(pos)
        if pos>0:
            titolo=titoli_model()
            #ricavo il collegamento
            pos=tmp.find('href="')
            pos2=tmp.find('"',pos+6)
            titolo.link=tmp[pos+6:pos2]
            if link_type==1:
                titolo.link=titolo.link.replace(site_base,'')
            titolo.link=str.replace(titolo.link,'?','&&')
            titolo.link=str.replace(titolo.link,'/','|')
            #print 'link' +  titolo.link
            
            #ricavo il titolo
            pos=tmp.find('class="titoloFilm">',pos2)
            pos2=tmp.find('</a>',pos+19)
            #print tmp[pos+7:pos2]
            titolo.titolo=tmp[pos+19:pos2]
           # pos2=tmp.find('</td>',pos)
            #print 'titolo ' + titolo.titolo
            #tmp=tmp[pos2:]
            res.append(titolo)
            
            #Ricavo l'anno
            stringa='<span class="vociFilm">ANNO:</span>'
            pos=tmp.find(stringa,pos2)
            pos2=tmp.find('</b>',pos+len(stringa))
            titolo.anno=tmp[pos+len(stringa):pos2]
            #print 'anno ' + titolo.anno
            tmp=tmp[pos2:]
            
        count=count+1
    
    return res