import urllib, urllister
from django.db import models
from django.conf import settings
import sys

import re
import wikipedia
import logging
path_base=settings.PATH_BASE
logger_download = logging.getLogger('movie_download')

def get_info_wikipedia(link):
    result={}
    foto_link={}
    persone={}
    try:
        site = wikipedia.getSite('it', 'wikipedia')
        page = wikipedia.Page(site, link)
    except:
        logger_download.warning(sys.exc_info())
    
    try:  
        #get(self, read_only=False, force=False, get_redirect=False, throttle=True)
        page_=page.get()
    except:
        logger_download.warning(sys.exc_info())
        page_=None
        result=None
        
    if page_!=None:
        #logger_download.info(page_)
        #logger_download.info(page.imagelinks())
        pos=page_.find('{{Film')
        
        count_persone=0
        count_foto=0
        result={}
        result['link']=link
        result['tipo']='wikipedia'
        result['titolo']=None
        result['titolo_originale']=None
        result['durata']=None
        result['anno']=None
        result['uscita']=None
        result['nazione']=None
        result['genere']=None
        result['descrizione']=None
        #logger_download.info(page_)
        if pos>=0:
            pos2=page_.find('}}',pos+6)
            film_data=page_[pos+6:pos2]
            #logger_download.info(film_data)
            film_data_list=film_data.split('|')
            for tmp in film_data_list:
                tmp=tmp.strip()
                if (tmp.find('immagine = ')==0):
                    foto_link[count_foto]='http://it.wikipedia.org/wiki/File:'+ tmp.replace('immagine = ','').replace(' ','_')
                    count_foto+=1
                    #logger_download.info(result['titolo'])
                
                if (tmp.find('titoloitaliano = ')==0):
                    result['titolo']=tmp.replace('titoloitaliano = ','')
                    logger_download.info(result['titolo'])
                
                if (tmp.find('titolooriginale = ')==0):
                    result['titolo_originale']=tmp.replace('titolooriginale = ','')
                    logger_download.info(result['titolo_originale'])
                
                if (tmp.find('durata = ')==0):
                    result['durata']=tmp.replace('durata = ','')
                    logger_download.info(result['durata'])
                    
                if (tmp.find('annouscita = ')==0):
                    anno_tmp=tmp.replace('annouscita = ','')
                    
                    anno_tmp = re.sub('\[\[([^\]\|]*)\]\]', '\\1', anno_tmp)
                    anno_tmp = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', anno_tmp)
                    result['anno']=anno_tmp
                    logger_download.info(result['anno'])
                    
                if (tmp.find('paese = ')==0):
                    nazione_tmp=tmp.replace('paese = ','')
                    nazione_tmp = re.sub('\[\[([^\]\|]*)\]\]', '\\1', nazione_tmp)
                    nazione_tmp = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', nazione_tmp)
                    result['nazione']=nazione_tmp
                    logger_download.info(result['nazione'])
                    
                if (tmp.find('genere = ')==0):
                    tmp2=tmp.replace('genere = ','')
                    
                    result['genere']=tmp2.split(',')[0]
                    logger_download.info(result['genere'])
                    
                if (tmp.find('regista = ')==0):
                    regia_tmp=tmp.replace('regista = ','')
                    
                    regia_tmp = re.sub('\[\[([^\]\|]*)\]\]', '\\1', regia_tmp)
                    regia_tmp = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', regia_tmp)
                    persone[count_persone,'link']=regia_tmp.replace(' ','_')
                    persone[count_persone,'nome']=regia_tmp
                    persone[count_persone,'professione']='REG'
                    persone[count_persone,'tipo_link']='wikipedia'
                    count_persone+=1
                    #logger_download.info(persone)
                
                if (tmp.find('produttore = ')==0):
                    prod_tmp=tmp.replace('produttore = ','')
                    prod_tmp_list=prod_tmp.split(',')
                    for prod in prod_tmp_list:
                        prod=prod.strip()
                        prod = re.sub('\[\[([^\]\|]*)\]\]', '\\1', prod)
                        prod = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', prod)
                        persone[count_persone,'link']=prod.replace(' ','_')
                        persone[count_persone,'nome']=prod
                        persone[count_persone,'professione']='PRO'
                        persone[count_persone,'tipo_link']='wikipedia'
                        count_persone+=1
                        
                if (tmp.find('attori = ')==0):
                    att_tmp=tmp.replace('attori = ','')
                    att_tmp_list=att_tmp.split('*')
                    for att in att_tmp_list:
                        #logger_download.info(att)
                        pos=att.find('[[')
                        if (pos>=0):
                            pos2=att.find(']]',pos+2)
                            att=att[pos+2:pos2]
                            persone[count_persone,'link']=att.replace(' ','_')
                            persone[count_persone,'nome']=att
                            persone[count_persone,'professione']='ATT'
                            persone[count_persone,'tipo_link']='wikipedia'
                            count_persone+=1         
                            #logger_download.info(att)
            
            #logger_download.info(persone)
            logger_download.info(foto_link)
        pos=page_.find('==Trama==')
        if (pos>=0):
            pos2=page_.find('== ',pos+9)
            trama=page_[pos+9:pos2]
            trama = re.sub('\[\[([^\]\|]*)\]\]', '\\1', trama)
            trama = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', trama)
            result['descrizione']=trama
        
    return result,persone
#    |titoloitaliano = I predatori dell'anno Omega
#|titoloalfabetico = Predatori dell'anno Omega, I
#|titolooriginale = Warrior of the Lost World<br />''(''Mad Rider ''titolo internazionale)'
#|immagine = I predatori dell'anno Omega.jpg
#|didascalia = il dittatore Prossor ([[Donald Pleasence]]) mentre tortura Nastasia ([[Persis Khambatta]])
#|linguaoriginale = inglese
#|paese = [[Italia]]
#|paese2 = [[Stati Uniti d'America|USA]]
#|annouscita = [[1983]]
#|durata = 92 min
#|tipocolore = colore
#|tipoaudio = sonoro
#|ratio = 1,85:1
#|genere = fantascienza, drammatico
#|regista = [[David Worth]]
#|soggetto = 
#|sceneggiatore = [[David Worth]]
#|produttore = [[Roberto Bessi]], [[Frank Hildebrand]]
#|produttoreesecutivo = 
#|casaproduzione = 
#|distribuzioneitalia = 
#|attori = 
#*[[Donald Pleasence]]: Prossor
#*[[Persis Khambatta]]: Nastasia
#|doppiatoriitaliani = 
#|fotografo = 
#|nome fonico = Muratori Primiano e Muratori Luciano
#|montatore = [[Cesare D'Amico]]
#|effettispeciali = 
#|musicista = [[Daniele Patucchi]]
#|temamusicale = 
#|scenografo = 
#|costumista = 
#|truccatore = 
#|sfondo = 
#|premi = 

    #logger_download.info(page_)
    
def get_pers_wikipedia(link):
    #print path_base
    #logger.info('Scarico il link ' + link)
    
    result={}
    tmp=link.split('|')
    if len(tmp)==2:
        site_lang=tmp[0]
        link=tmp[1]
    else:
        site_lang='it'
    try:
        site = wikipedia.getSite(site_lang, 'wikipedia')
        page = wikipedia.Page(site, link)
    except:
        logger_download.warning(sys.exc_info())
    
    #   datapage =wikipedia.DataPage(site, link)
    #    datapage_=datapage.get()
    result['biografia']=None
    result['nome']=None
    result['cognome']=None
    result['sesso']=None
    result['luogo_nascita']=None
    result['data_nascita']=None
    result['link_foto']=None
    try:  
        page_=page.get()
    except:
        logger_download.warning(sys.exc_info())
    pos=page_.find('{{Bio')
    offset=5
    if pos<0:
        pos=page_.find('{{Infobox person')
        offset=16
    #print page_
    if pos>=0:
        #print 'nnnn'
        pos2=page_.find('\n}}',pos+offset)
        bio=page_[pos+offset:pos2]
        #print bio
        logger_download.info(bio)
        bio_list=bio.split('|')
        for tmp in bio_list:
            tmp=tmp.strip()
            logger_download.info(tmp)
            if (tmp.find('Nome = ')==0):
                result['nome']=tmp.replace('Nome = ','')
                
            if (tmp.find('Cognome = ')==0):
                result['cognome']=tmp.replace('Cognome = ','')
               # print result['cognome']
                
            if (tmp.find('Sesso = ')==0):
                result['sesso']=tmp.replace('Sesso = ','')
                #print result['sesso']
            
            #name in inglese
            m=re.match(r"(\bname\b\s*=\s*)([\w\s\']*)",tmp)
            if m!=None:
                result['nome']=m.group(2)
                
                logger_download.info(result['nome'])
                
            if (tmp.find('LuogoNascita = ')==0):
                result['luogo_nascita']=tmp.replace('LuogoNascita = ','')
                #print result['luogo_nascita']
                
            m=re.match(r"(\bbirth_place\b\s*=\s*)",tmp)
            if m!=None:
                result['luogo_nascita']=re.sub(r"(\bbirth_place\b\s*=\s*)",'',tmp).replace('[','').replace(']','')
                logger_download.info(result['luogo_nascita'])
            
            
            if (tmp.find('GiornoMeseNascita = ')==0):
                GiornoMeseNascita=tmp.replace('GiornoMeseNascita = ','')
                
            if (tmp.find('AnnoNascita = ')==0):
                AnnoNascita=tmp.replace('AnnoNascita = ','')
            
            #print tmp
    
    tmp_bio=None
    
    word_list=['== Biografia ==','==Career==','==Biografia==']
    pos=-1
    for word in word_list:
        if pos==-1:
            pos=page_.find(word)
            offset=len(word)
    
    
    if pos>0:
        pos2=page_.find('==',pos +offset)
        tmp_bio=page_[pos+offset:pos2-1].strip()
    
    if tmp_bio!=None:
        tmp_bio = re.sub('\[\[([^\]\|]*)\]\]', '\\1', tmp_bio)
        tmp_bio = re.sub('\[\[(?:[^\]\|]*)\|([^\]\|]*)\]\]', '\\1', tmp_bio)
        tmp_bio=tmp_bio.replace("''","'")
        #print tmp_bio
        result['biografia']=tmp_bio
    else:
        result['biografia']=None
    try:
        file=open(path_base+'tmp/wikipers.html',mode="wb")
        file.write(page_.encode('ascii','ignore'))
        file.close()
    except:
        pass
    #logger_download.info(page.imagelinks())
    #logger_download.info(page_)
    return result