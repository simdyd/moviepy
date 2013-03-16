from django.conf import settings
from django.db import models
import urllib
import urllister

site_base='http://www.mymovies.it/'
path_base=settings.PATH_BASE

def get_info_mymovies(link,link_type=1):
    link=str(link).replace('&&','?')
    link=str(link).replace('|','/')
    if link_type==1:
        link=site_base+link
    #print 'link' + link
    urllib.urlretrieve(link,path_base+'tmp/file_info_mymovies.html')
    input=open(path_base+'tmp/file_info_mymovies.html')
    result={}
    persone={}
    foto_link={}
    count_persone=0
    result['link']=link
    result['tipo']='mymovies'
    #print link
    
    pagina=input.read()
    #recupero il titolo
    #<h1 style="margin-bottom:3px;">
    pos=pagina.find('<h1 ')
    pos2=pagina.find('</h1>',pos+31)
    result['titolo']=pagina[pos+31:pos2].strip().decode(encoding='iso-8859-1',errors='strict')
    #print result['titolo']
    
    #Dettagli
    stringa='<div style="text-align:justify" class="linkblu">'
    pos=pagina.find(stringa)
    pos2=pagina.find("<table",pos)
    tmp=pagina[pos:pos2]
    #print tmp
    #titolo originale
    stringa='Titolo originale <em>'
    pos=tmp.find(stringa)
    if pos>0:
        pos2=tmp.find('</em>',pos)
        result['titolo_originale']=tmp[pos+len(stringa):pos2].strip().decode(encoding='iso-8859-1',errors='strict')
        #print result['titolo_originale']
    else:
        result['titolo_originale']=result['titolo']
    
    #durata
    stringa='durata '
    pos=tmp.find(stringa)
    pos2=tmp.find('.',pos)
    result['durata']=tmp[pos+len(stringa):pos2].strip()
    
    #Nazione
    #- USA  <strong>
    pos3=tmp.find('-',pos2)
    pos4=tmp.find('<strong>',pos3)
    result['nazione']=tmp[pos3+1:pos4].strip() 
    
    #provo anno e categoria
    stringa='<a title="Film'
    pos=tmp.find(stringa)
    while pos>0:
        pos2=tmp.find('>',pos)
        pos3=tmp.find('</a>',pos2)
    
        test= tmp[pos2+1:pos3].strip()
        try:
            test2=int(test)
             
            result['anno']=test2
        except:
            result['genere']=test
            
        pos=tmp.find(stringa,pos3)
    
    #Regia
    stringa="Un film di"
    pos=tmp.find(stringa)
    
    pos3=tmp.find('<a href="',pos)
    if pos3>0: #ho trovato il link
        pos4=tmp.find('"',pos3+9)
        link=tmp[pos3+9:pos4].strip()
        pos4=tmp.find('>',pos3)
        pos5=tmp.find('</a>',pos4)
        tmp2=tmp[pos4+1:pos5]
        
    else:
        pos2=tmp.find(".",pos+len(stringa))
    
    
        tmp2=tmp[pos+len(stringa):pos2].strip()
            
        link=''
    print tmp2
    print link
    
    persone[count_persone,'nome']=tmp2
    persone[count_persone,'professione']='REG'
    persone[count_persone,'tipo_link']='mymovies'
    persone[count_persone,'link']=link
    
    count_persone=count_persone+1
    
    #Attori
    stringa="Con <a"
    pos=tmp.find(stringa)
    pos2=tmp.find("<div",pos)
    tmp2=tmp[pos:pos2]
    pos=tmp2.find('<a href="')
    while (pos>0):
        pos_=tmp2.find('>',pos)
        pos2=tmp2.find('<',pos_)
        attore=tmp2[pos_+1:pos2]
        if attore!='</a>':
            
            pos3=tmp2.find('"',pos+9)
            persone[count_persone,'link']=tmp2[pos+9:pos3].strip()
            persone[count_persone,'nome']=attore
            persone[count_persone,'professione']='ATT'
            persone[count_persone,'tipo_link']='mymovies'
            #print persone[count_persone,'link']
            count_persone=count_persone+1
        tmp2=tmp2[pos2:]
        
        pos=tmp2.find('<a href="') 
    stringa='<div id="recensione">'
    #Locandina
    
    #Trova link locandina
    pos=pagina.find(stringa)
    stringa2='<img style="'
    pos=pagina.find(stringa2,pos)
    pos2=pagina.find('src="',pos)
    pos3=pagina.find('"',pos2+5)
    tmp=pagina[pos2+5:pos3].strip()
    foto_link[0]=tmp
    #print foto_link[0]
    
    #Trama 
    pos=pagina.find(stringa)
    pos=pagina.find("<p>",pos)
    pos2=pagina.find("</p>",pos+3)
    result['descrizione']=pagina[pos+3:pos2].strip().decode(encoding='iso-8859-1',errors='strict')
    #print result['descrizione']
    
    return result,persone,foto_link