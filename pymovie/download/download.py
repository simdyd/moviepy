import urllib, urllister
from django.db import models
from django.conf import settings
#from film.models import * 
#usock = urllib.urlopen("http://www.35mm.it/search/?string=ember&year=0&month=0&day=0&sections[]=film&open_tab=0/")

path_base=settings.PATH_BASE
site_base='http://film.35mm.it/'
import logging
logger_download = logging.getLogger('movie_download')
logger = logging.getLogger('movie')

def get_link_foto_pers_35mm(link,link_type=0):
    urllib.urlretrieve(link,path_base+'tmp/file_foto_pers_35mm.html')
    #input=open(path_base+'tmp/file_foto_35mm.html')
    input=open(path_base+'tmp/file_foto_pers_35mm.html')
    pagina=input.read()
    count=0
    foto_link={}
    
    pos=pagina.find('var listOfImages = [')
    #print 'pos' + pos
    if pos>0:
        
        pos2=pagina.find('];',pos)
        blocco=pagina[pos:pos2]
        blocco=blocco.replace("'",'')
        tmp=blocco.split(',')
        dim=len(tmp)
        #print blocco
        #print dim
        i=0
        while i<dim:
            foto_link[count]=site_base+tmp[i][1:]
            #foto_link[count]=foto_link[count].replace('//','/')
            #print foto_link[count]
            i=i+1
            count=count+1
    
            
   
    return foto_link

def get_link_foto_35mm(link,link_type=0):
    #print 'get link foto 35mm'
    urllib.urlretrieve(link,path_base+'tmp/file_foto_35mm.html')
    input=open(path_base+'tmp/file_foto_35mm.html')
    pagina=input.read()
    count=0
    foto_link={}
    
    pos=pagina.find('var listOfImages = [')
    #print 'pos' + pos
    if pos>0:
        
        pos2=pagina.find('];',pos)
        blocco=pagina[pos:pos2]
        blocco=blocco.replace("'",'')
        tmp=blocco.split(',')
        dim=len(tmp)
        #print blocco
        #print dim
        i=0
        while i<dim:
            foto_link[count]=site_base+tmp[i][1:]
            #foto_link[count]=foto_link[count].replace('//','/')
            #print foto_link[count]
            i=i+1
            count=count+1
    
    if count==0:
        pos=pagina.find('<div id="thumbs_button_left"')
        pos2=pagina.find('<div id="thumbs_button_right"',pos)
        blocco=pagina[pos:pos2]
        result='ok'
        while result=='ok':
            stringa='<img src="'
            pos=blocco.find(stringa)
            if pos>0:
                pos2=blocco.find('"',pos+len(stringa))
                if link_type==0:
                    foto_link[count]=site_base+(blocco[pos+len(stringa)+1:pos2]).replace(' ','%20')
                else:
                    foto_link[count]=(blocco[pos+len(stringa):pos2])
                #print foto_link[count]
                count=count+1
                blocco=blocco[pos2:]
            else:
                result='ko'
            
   
    return foto_link

def get_pers_35mm(link):
    #print path_base
    #logger.info('Scarico il link ' + link)
    
    urllib.urlretrieve(link,path_base+'tmp/file_pers_35mm.html')
    input=open(path_base+'tmp/file_pers_35mm.html')
    result={}
    pagina=input.read()
    #Ricavo il link della foto
    stringa='<div id="cover_left">'
    pos=pagina.find(stringa)
    pos2=pagina.find('</div>',pos)
    tmp=pagina[pos+len(stringa):pos2].strip()
    #print 'tmp' + tmp
    stringa='src="'
    pos=tmp.find(stringa)
    pos2=tmp.find('"',pos+len(stringa))
    result['link_foto']=site_base+tmp[pos+len(stringa):pos2].strip()
    pos=result['link_foto'].find('tappo_img_star')
    if (pos>0):
        result['link_foto']=None
    #print 'link ' + result['link']
    
    #Biografia
    stringa='<div id="main_m">'
    pos=pagina.find(stringa)
    stringa='<div class="description">'
    pos2=pagina.find(stringa,pos)
    pos3=pagina.find('</div>',pos2)
    result['biografia']=pagina[pos2+len(stringa):pos3].strip()
    if (result['biografia']=="<div style=\"text-align: center;\">biografia del personaggio non inserita"):
        result['biografia']=None
    
    #Parte con i dettagli sull'attore
    pos=pagina.find('<ul class="details">')
    pos2=pagina.find('</ul>',pos)
    tmp=pagina[pos:pos2].strip()
    
    #Nome
    stringa='<span>Nome:</span>'
    pos=tmp.find(stringa)
    if (pos>0):
        pos2=tmp.find('</li>',pos)
        result['nome']=tmp[pos+len(stringa):pos2].strip()
    else:
        result['nome']=None
        
    #Cognome
    stringa='<li><span>Cognome:</span>'
    pos=tmp.find(stringa)
    if (pos>0):
        pos2=tmp.find('</li>')
        result['cognome']=tmp[pos+len(stringa):pos2].strip()
    else:
        result['cognome']=None
    #Sesso
    stringa='<li><span>Sesso:</span>'
    pos=tmp.find(stringa)
    if (pos>0):
        pos2=tmp.find('</li>',pos)
        result['sesso']=tmp[pos+len(stringa):pos2].strip()
    else:
        result['sesso']=None
    #print result['sesso']
    
    #<li><span>Luogo di nascita:</span> 
    stringa='<li><span>Luogo di nascita:</span>'
    pos=tmp.find(stringa)
    if (pos>0):
        pos2=tmp.find('</li>',pos)
        result['luogo_nascita']=tmp[pos+len(stringa):pos2].strip()
    else:
        result['luogo_nascita']=None
    #<li><span>Data di nascita:</span>
    stringa='<li><span>Data di nascita:</span>'
    pos=tmp.find(stringa)
    if (pos>0):
        pos2=tmp.find('</li>',pos)
        result['data_nascita']=tmp[pos+len(stringa):pos2].strip()
    else:
        result['data_nascita']=None
    
    
    #print '------------------------------------------------'
    #print tmp
    #print '------------------------------------------------'
    return result

def get_attori_list_old(pagina,persone,count_persone):
    stringa='<div class="mod_castcrew_tab" id="mod_castcrew_tab_cast"'
    pos=pagina.find(stringa)
       
    pos2=pagina.find('<div class="mod_castcrew_tab" id="mod_castcrew_tab_crew"',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    stringa="<li>"
    go=True
    while go==True:
        pos=tmp.find(stringa)
        #print 'pos' + str(pos) 
        if (pos>0):
            pos2=tmp.find('</li>',pos+len(stringa))
            blocco_tmp=tmp[pos+len(stringa):pos2]
            tmp=tmp[pos2:]
            #print blocco_tmp
            pos=blocco_tmp.find('<h4>')
            pos2=blocco_tmp.find('</h4>',pos+4)
            blocco_tmp=blocco_tmp[pos+4:pos2]
            pos=blocco_tmp.find('>')
            pos2=blocco_tmp.find('<',pos+1)
            persone[count_persone,'nome']=blocco_tmp[pos+1:pos2]
            #print persone[count_persone,'nome']
            pos=blocco_tmp.find('href="')
            pos2=blocco_tmp.find('"',pos+len('href="'))
            persone[count_persone,'link']=blocco_tmp[pos+len('href="'):pos2]
            #print persone[count_persone,'link']
            persone[count_persone,'professione']='ATT'
            persone[count_persone,'tipo_link']='35mm'
            count_persone+=1
            
        else:
            go=False
    
    return persone,count_persone

def get_attori_list_35mm(link,persone,count_persone):
    urllib.urlretrieve(link,path_base+'tmp/file_list_persone_35mm.html')
    input=open(path_base+'tmp/file_list_persone_35mm.html')
    pagina=input.read()
    
    
    stringa='<li class="list_type">CAST</li>'
    pos=pagina.find(stringa)
    if pos<0:
        stringa='<li class="list_type">ATTORI PROTAGONISTI</li>'
        pos=pagina.find(stringa)
        
    pos2=pagina.find('<li class="list_type">CREW</li>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    input.close()
    stringa='<li class="list_filmografy">'
    
    go=True
    while go==True:
        pos=tmp.find(stringa)
        #print 'pos' + str(pos) 
        if (pos>0):
            pos2=tmp.find('</li>',pos+len(stringa))
            blocco_tmp=tmp[pos+len(stringa):pos2]
            tmp=tmp[pos2:]
            #print blocco_tmp
            pos=blocco_tmp.find('href="')
            pos2=blocco_tmp.find('"',pos+len('href="'))
            persone[count_persone,'link']=blocco_tmp[pos+len('href="'):pos2]
            
            pos3=blocco_tmp.find('>',pos2)+1
            pos4=blocco_tmp.find('<',pos3)
            #ppp=blocco_tmp[pos3:pos4]
            #logger_download.info( ppp)
            if blocco_tmp[pos3:pos4]!='':
                persone[count_persone,'nome']=blocco_tmp[pos3:pos4]
                persone[count_persone,'professione']='ATT'
                persone[count_persone,'tipo_link']='35mm'
                count_persone+=1
        else:
            go=False
        
    return persone,count_persone

def get_info_35mm(link,link_type=1):
    if link_type==1:
        link=site_base+link
    urllib.urlretrieve(link,path_base+'tmp/file_info_35mm.html')
    input=open(path_base+'tmp/file_info_35mm.html')
    result={}
    persone={}
    foto_link={}
    count_persone=0
    result['link']=link
    pagina=input.read()
    #titolo
    pos=pagina.find('<li><span>Titolo:</span>')
    pos2=pagina.find('</li>',pos+24)
    result['titolo']=pagina[pos+24:pos2].strip()
    #print result['titolo']
    
    #titolo originale
    stringa='<li><span>Titolo originale:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    result['titolo_originale']=pagina[pos+len(stringa):pos2].strip()
    #print result['titolo_originale']
    
    #durata
    stringa='<li><span>Durata:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2].strip()
    result['durata']=tmp[:20]
    #print result['durata']
    
    #anno
    stringa='<li><span>Anno di produzione:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    result['anno']=pagina[pos+len(stringa):pos2].strip()
    #print result['anno']

    #uscita
    stringa='<li><span>Uscita:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    result['uscita']=pagina[pos+len(stringa):pos2].strip()
    #print result['uscita']
    
    #Nazione
    stringa='<span>Nazione:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</li>',pos+len(stringa))
    result['nazione']=pagina[pos+len(stringa):pos2].strip()
    #print result['nazione']
    
    #Genere
    #<a href="http://film.35mm.it/generi/fantascienza.html" title="Fantascienza">Fantascienza</a>
    stringa='<span>Genere:</span>'
    pos=pagina.find(stringa)
    pos2=pagina.find('</a>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2].strip()
    pos=tmp.find('>')
    result['genere']=tmp[pos+1:]
    #print result['genere']
    
    #Regia
    stringa='<span>Regia:</span>'
    pos=pagina.find(stringa)
    if (pos>0):
        pos2=pagina.find('</a>',pos+len(stringa))
        tmp=pagina[pos+len(stringa):pos2].strip()
        stringa='href="'
        pos=tmp.find(stringa)
        pos2=tmp.find('"',pos+len(stringa))
        persone[count_persone,'link']=tmp[pos+len(stringa):pos2]
        #print persone[count_persone,'link']
    
        stringa='title="'
        pos=tmp.find(stringa)
        pos2=tmp.find('"',pos+len(stringa))
        persone[count_persone,'nome']=tmp[pos+len(stringa):pos2]
        persone[count_persone,'professione']='REG'
        persone[count_persone,'tipo_link']='35mm'
        #print persone[count_persone,'nome']
        count_persone=count_persone+1
    #descrizione
    stringa='<div class="description">'
    pos=pagina.find(stringa)
    pos2=pagina.find('</div>',pos+len(stringa))
    result['descrizione']=pagina[pos+len(stringa):pos2].replace (chr(13)+chr(10),' ')
    #print result['descrizione']
    
    #link foto
    stringa='<a id="gallery" href="'
    pos=pagina.find(stringa)
    pos2=pagina.find('"',pos+len(stringa))
    result['gallery_link']=pagina[pos+len(stringa):pos2]
    #print result['gallery_link']
    
    #Link Locandina
    #Trova link locandina
    #<img alt="Immagine Scheda" style="top: 30px; left: 30px;" src="/immagini/film/m25915.gif">
    stringa='<div id="cover">'#style="top: 30px; left: 30px;" src="/immagini/film/m25915.gif">'
    pos=pagina.find(stringa)
    pos2=pagina.find("</div>",pos)
    tmp=pagina[pos:pos2]
    
    
    pos2=tmp.find('href="')
    if pos2>0:
        pos3=tmp.find('"',pos2+6)
        #print pos2
        #print pos3
        tmp=tmp[pos2+7:pos3]
        
        #print tmp
        if tmp!='avascript:void(0)':
            logger_download.info('trovata locandina ' + tmp)
            #logger_download.info(tmp)
            foto_link[0]=site_base+tmp
            #print foto_link[0]
    
    #inizio cast
        
    link_attori=link.replace('.html','/cast-crew-lista-completa.html')
    #persone,count_persone=get_attori_list_old(pagina,persone,count_persone)
    persone,count_persone=get_attori_list_35mm(link_attori,persone,count_persone)
    #<div class="mod_castcrew_tab" id="mod_castcrew_tab_crew"
    
    #inizio crew
    #<div class="mod_castcrew_tab" id="mod_castcrew_tab_crew"
    stringa='<div class="mod_castcrew_tab" id="mod_castcrew_tab_crew"'
    pos=pagina.find(stringa)
    pos2=pagina.find('</ul>',pos+len(stringa))
    tmp=pagina[pos+len(stringa):pos2]
    stringa="<li>"
    go=True
    while go==True:
        pos=tmp.find(stringa)
        if (pos>0):
            pos2=tmp.find('</li>',pos+len(stringa))
            blocco_tmp=tmp[pos+len(stringa):pos2]
            tmp=tmp[pos2:]
            #Recupero la professione
            pos=blocco_tmp.find('<small>')
            pos2=blocco_tmp.find('</small>',pos+7)
            prof_tmp=blocco_tmp[pos+7:pos2]
            #print prof_tmp
            if prof_tmp=='Sceneggiatura':
                persone[count_persone,'professione']='SCE'
            elif prof_tmp=='Montaggio':
                persone[count_persone,'professione']='MON'
            elif prof_tmp=='Musiche':
                persone[count_persone,'professione']='MUS'
            elif prof_tmp=='Prodotto da':
                persone[count_persone,'professione']='PRO'
            elif prof_tmp=='Fotografia':
                persone[count_persone,'professione']='FOT'
            else:
                #print 'Professione Sconosciuta'
                persone[count_persone,'professione']='NAN'
            persone[count_persone,'tipo_link']='35mm'
            #print blocco_tmp
            #print persone[count_persone,'professione']
            pos=blocco_tmp.find('<h4>')
            pos2=blocco_tmp.find('</h4>',pos+4)
            blocco_tmp=blocco_tmp[pos+4:pos2]
            pos=blocco_tmp.find('>')
            pos2=blocco_tmp.find('<',pos+1)
            persone[count_persone,'nome']=blocco_tmp[pos+1:pos2]
            #print persone[count_persone,'nome']
            pos=blocco_tmp.find('href="')
            pos2=blocco_tmp.find('"',pos+len('href="'))
            persone[count_persone,'link']=blocco_tmp[pos+len('href="'):pos2]
            #print persone[count_persone,'link']
            
            
            count_persone+=1
            
        else:
            go=False
    result['tipo']='35mm'
    #<div id="show_all">
    #print count_persone
    return result,persone,foto_link

class titoli_model():
    id = models.AutoField(primary_key=True)
    titolo = models.TextField()
    link = models.TextField()
    anno = models.TextField()
    note = models.TextField()
    
    

def trova_titoli_35mm(titolo,link_type=1):
    titolo=titolo.replace(' ','+')
    
    urllib.urlretrieve("http://www.35mm.it/search/?string="+titolo+"&year=0&month=0&day=0&sections[]=film&open_tab=0/",path_base+'tmp/file_35mm.html')
    input=open(path_base+'tmp/file_35mm.html')
    pagina=input.read()

    #Ricavo la parte interessante nella ricerca
    pos=pagina.find('<!-- Start result film -->')
    pos2=pagina.find('<!-- End result film -->')
    risultati=pagina[pos:pos2]

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

#elenco=trova_titoli_35mm ('ember')

#get_info_35mm('http://film.35mm.it/ember-il-mistero-della-citta-di-luce-2008.html',0)
#for url in parser.urls: print 'link ' + url

#for img in parser.imgs: print 'img ' + img