from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from download.download import *
from download.download_filmtv import *
from download.download_imdb import *
from download.download_mymovies import *
from download.downloadcoming import *
if settings.USE_WIKIPEDIA==True:
    from download.download_wikipedia import get_info_wikipedia
from film.forms import SearchForm
from film.models import *
from media.models import Photo
from persone.models import *
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import Image
import datetime
import os
import sys
import traceback
import urllib

import logging
logger_download = logging.getLogger('movie_download')
logger = logging.getLogger('movie')

def get_default_parameter():
    parameters={}
    generi_list=Genere.objects.all()
    supporti_list=Supporti.objects.exclude(gruppo='supporti')
    form=SearchForm()
    parameters['generi_list'] = generi_list
    parameters['supporti_list'] = supporti_list
    parameters['form'] = form
    return parameters

#detect dispositivi mobili...

def dashboard(request):
    parameters=get_default_parameter()
    
    totale_film=Movie.objects.all().count()
    
    film_foto=MovieFoto.objects.all().values('movie').distinct().count()
    film_loca=MovieFoto.objects.filter(tipo='locandina').values('movie').distinct().count()
    
    film_no_foto=totale_film-film_foto
    film_no_loca=totale_film-film_loca
    film_no_ori=Movie.objects.filter(video_file=None).count()
    
    parameters['totale_film'] = totale_film
    parameters['film_foto'] = film_foto
    parameters['film_loca'] = film_loca
    parameters['film_no_loca'] = film_no_loca
    parameters['film_no_foto'] = film_no_foto
    parameters['film_no_ori'] = film_no_ori
    
    
    parameters['page_tipe'] = 'dashboard'
    #parameters['form'] = form
    #parameters['film_list'] = items
    parameters['genere']=0
    parameters['kindlist']='no_video'
    parameters['supporto']=0
    
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


#from bloom.device.decorators import detect_device
def get_film_senza_video(request):
    
    film_list=Movie.objects.filter(video_file=None).order_by('-anno')
    
    if film_list!=None:            
        items=get_pagination_film(1,film_list)
    else:
        items=None
    
    
    parameters=get_default_parameter()
    
    
    
    parameters['page_tipe'] = 'home'
    #parameters['form'] = form
    parameters['film_list'] = items
    parameters['genere']=0
    parameters['kindlist']='no_video'
    parameters['supporto']=0
    
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


def get_film_senza_thumbnail(request):
    mf_list=MovieFoto.objects.all().values('movie').distinct()
    #film_list=''
    film_list=[]
    for mf in mf_list:
        #if film_list!='':
        #    film_list+=','
        #film_list+=str(mf['movie'])
        film_list.append(mf['movie'])
    logger.info(film_list)
    
    film_list=Movie.objects.exclude(id__in=film_list)
    
    if film_list!=None:            
        items=get_pagination_film(1,film_list)
    else:
        items=None
    
    
    parameters=get_default_parameter()
    
    
    
    parameters['page_tipe'] = 'home'
    #parameters['form'] = form
    parameters['film_list'] = items
    parameters['genere']=0
    parameters['kindlist']='no_thumbnail'
    
    parameters['supporto']=0
    
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def get_film_senza_locandine(request):
    mf_list=MovieFoto.objects.filter(tipo='locandina').values('movie').distinct().order_by('movie')
    #film_list=''
    film_list=[]
    for mf in mf_list:
        #if film_list!='':
        #    film_list+=','
        #film_list+=str(mf['movie'])
        film_list.append(mf['movie'])
    logger.info(film_list)
    
    film_list=Movie.objects.exclude(id__in=film_list)
    
    if film_list!=None:            
        items=get_pagination_film(1,film_list,10)
    else:
        items=None
    
    
    parameters=get_default_parameter()
    
    
    
    parameters['page_tipe'] = 'home'
    #parameters['form'] = form
    parameters['film_list'] = items
    parameters['genere']=0
    
    parameters['kindlist']='no_loca'
    parameters['supporto']=0
    
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


def ricava_parametri_video(movie):
    #recupero i media associati
    movie_media_list=MovieMedia.objects.filter(tipo='orig',movie=movie)
    #print 'param video'
    for movie_media in movie_media_list:
        if movie_media.file_durata==None:
            ffmpeg = "ffmpeg -i '%s'" %(movie_media.file)
            #print ffmpeg
            ffmpegresult = commands.getoutput(ffmpeg)
            pos=ffmpegresult.find('Input #0,')
            pos2=ffmpegresult.find('Output #0',pos)
            tmp=ffmpegresult[pos+len('Input #0,'):pos2].strip()
            
            #print tmp
            #durata
            pos=tmp.find('Duration: ')
            pos2=tmp.find(',',pos)
            movie_media.file_durata=tmp[pos+len('Duration: '):pos2].strip()
            #print 'durata : ' + durata
            
            #bitrate
            pos=tmp.find('bitrate: ')
            pos2=tmp.find('s',pos)
            movie_media.file_bitrate=tmp[pos+len('bitrate: '):pos2+1].strip()
            #print 'bitrate : ' + bitrate
            
            #Dettagli video
            pos=tmp.find('Video: ')
            pos2=tmp.find(chr(10),pos)
            movie_media.file_video=tmp[pos+len('Video: '):pos2].strip()
            #print 'video : ' + Video
            
            #Dettagli audio
            pos=tmp.find('Audio: ')
            pos2=tmp.find(chr(10),pos)
            movie_media.file_audio=tmp[pos+len('Audio: '):pos2].strip()
            #print 'Audio : ' + Audio
           
            movie_media.save()

def supporto_pdf(request,supporto_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,pagesize=A4)

    #drawImage(self, image, x, y, width=None, height=None, mask=None, preserveAspectRatio=False, anchor='c')
    #img=Image.open("/var/www/html/moviepy/static/grafica/hellboy.jpeg")
    #A4 = (595.275590551, 841.88976378)
    p.rect(10,10, 10 * mm,20* mm)
    #p.drawImage(img, 300, 100)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def theme(parameters):
    
    parameters['bgcolor1']="#FFFFFF"
    parameters['bgcolor2']="#ccccff"
    parameters['bgcolor3']="#ccffcc"
    parameters['bgcolor4']="#dfdfdf"
    parameters['bgcolor5']="#80802b"
    parameters['bgcolor6']="#c8c85b"
    parameters['bgcolor7']="#e3e3FF"
    
    parameters['textcolor1']="FFFFFF"
    parameters['textcolor2']="000000"
    
    parameters['bordercolor1']="#FFFFFF"
    parameters['bordercolor2']="#cccccc"
    return parameters

def save_persone_ext(film,persone):
    print 'Salvataggio Persone'
    if persone:
        count=0
        ok=True
        while ok==True and count<50:
            try:
                persona=None
                try:
                    tmp=persone[count,'nome'].find(' ')
                    if tmp>0:
                        nome=persone[count,'nome'][:tmp].strip()
                        cognome=persone[count,'nome'][tmp:].strip()
                    else:
                        nome=persone[count,'nome'].strip()
                        cognome=''
                except:
                    nome=None
                    cognome=None
                
                
                if (nome!=None and cognome!=None):
                    try:
                        persona=Persona.objects.get(nome=nome,cognome=cognome)
                        #print persona.nometNpers=Fals
                        try:
                            persona_link=PersonaLink.objects.get(persona=persona,tipo_link=persone[count,'tipo_link'])
                            
                            persona_link.link=persone[count,'link']
                            #persona.download=0
                            persona_link.save()
                        except:
                            logger_download.warning('Link non trovato')
                            logger_download.warning(sys.exc_info())
                            
                            persona_link=PersonaLink()
                            persona_link.persona=persona
                            persona_link.tipo_link=persone[count,'tipo_link']
                            persona_link.link=persone[count,'link']
                            persona_link.download=0
                            persona_link.save()
                            #print sys.exc_info()
                            #print 'problemi nel salvataggio del link'
                            
                    except ObjectDoesNotExist:
                        #print sys.exc_info()
                        try:
                            persona=Persona()
                            #print nome + ' ' + cognome + ' ' + persone[count,'link']
                            persona.nome=nome
                            persona.cognome=cognome
                            #persona.download=0
                            #persona.link=persone[count,'link']
                            #persona.tipo_link=persone[count,'tipo_link']
                            persona.save()
                        except:
                            persona=None
                            logger_download.warning('Problema creazione nuova persona')
                            logger_download.warning(sys.exc_info())
                            
                        if persona!=None:
                            persona_link=PersonaLink()
                            persona_link.persona=persona
                            persona_link.tipo_link=persone[count,'tipo_link']
                            persona_link.link=persone[count,'link']
                            persona_link.download=0
                            persona_link.save()
                    except:
                        logger_download.warning('Problema a trovare la persona')
                        logger_download.warning(sys.exc_info())
                        
                #else:
                #    logger_download.warning('Problema nome e cognome ')
                        
                if persona!=None:
                    try:    
                        professione=Professioni.objects.get(short_id=persone[count,'professione'])
                        persona.professione.add(professione)
                        persona.save()
                    except:
                        #print sys.exc_info()
                        pass
                    try:
                        if persone[count,'professione']=='ATT':
                            film.attori.add(persona)
                            film.save()
                        elif persone[count,'professione']=='REG':
                            film.regia.add(persona)
                            film.save()
                        elif persone[count,'professione']=='SCE':
                            film.sceneggiatura.add(persona)
                            film.save()
                        elif persone[count,'professione']=='MUS':
                            film.musica.add(persona)
                            film.save()
                        elif persone[count,'professione']=='FOT':
                            film.fotografia.add(persona)
                            film.save()
                        elif persone[count,'professione']=='PRO':
                            film.produttore.add(persona)
                            film.save()
                    except:
                        #impossibile salvare il film
                        #print sys.exc_info()
                        pass
                
                    #print nome + ' _ ' + cognome + ' ____ ' + persone[count,'professione']
                count=count+1
            except:
                
                logger_download.warning(sys.exc_info())
                logger_download.warning(persona)
                
                ok=False
            
def save_film_ext(film,dati):
    if dati:
        film.titolo=dati['titolo']
        if (dati['titolo_originale']!=None):
            film.titolo_originale=dati['titolo_originale']
        if dati['durata']!=None:
            film.durata=dati['durata']
        if dati['anno']!=None:
            try:
                film.anno=int(dati['anno'])
            except:
                print 'problemi con l\'anno'
        if dati['link']!=None:
            try:
                link=MovieLink.objects.get(movie=film,tipo=dati['tipo'])
                link.download=True
            except:
                link=MovieLink()
                link.movie=film
                link.tipo=dati['tipo']
                link.download=True
            link.link=dati['link']
            link.save()
        #dati['uscita']
        if dati['nazione']!=None:
            film.paese=dati['nazione'][:20]
        if dati['genere']!=None:
            generi_list=[]
            
            for genere_tmp in dati['genere'].split(','):
                genere_tmp=genere_tmp.strip()[:20]
                try:
                    genere=Genere.objects.get(nome=genere_tmp)
                except:
                    genere=Genere()
                    genere.nome=genere_tmp
                    genere.save()
                generi_list.append(genere)
            #print 'id genere ' + str(genere.id)
            film.genere=generi_list
        if dati['descrizione']!=None:
            film.trama=dati['descrizione']
        else:
            film.trama=''
        try:
            film.download=1
            film.save()
        except:
            print sys.exc_info()

def download_foto(film,link_foto,tipo='classic'):
    #print 'download foto'
    count=0
    ok=True
    new_file_dir = os.path.dirname(settings.MEDIA_ROOT+film.data_ins.strftime("%Y"+os.sep+"%m"+os.sep))
    if not os.path.exists(new_file_dir):
        os.makedirs(new_file_dir)
    while ok==True:
        try:
            link=link_foto[count]
            pos=link.rfind('/')
            nome_foto=link[pos+1:]
            try:
                
                nome_foto=nome_foto.replace('%20','_')
                name = film.data_ins.strftime("%Y"+os.sep+"%m"+os.sep) + str(film.id) + nome_foto
                try:
                    image = urllib.URLopener()
                    image.retrieve(link,settings.MEDIA_ROOT + name)
                except:
                    image=None
                    logger_download.warning('foto non trovata')
                    logger_download.warning(sys.exc_info())
                    logger_download.info(link)
                #print link
                if image!=None:
                    try:
                        img = Photo.objects.get(image=name)
                    except:    
                        img = Photo()
                        img.name = nome_foto
                        img.image=name
                        img.upload_date = datetime.datetime.now()
                        img.publish_date = datetime.datetime.now()
                        img.save()
                        
                    #film.foto.add(img)
                    #film.save()
                    if img!=None:
                        try:
                            moviefoto=MovieFoto.objects.get(foto=img,movie=film)
                        except:
                            #nonlotrovo lo aggiungo
                            moviefoto=MovieFoto()
                            moviefoto.foto=img
                            moviefoto.movie=film
                            if tipo=='classic':
                                moviefoto.ordine=100
                            elif tipo=='locandina':
                                moviefoto.ordine=10
                            moviefoto.tipo=tipo
                            moviefoto.save()
                
            except:
                logger_download.warning('Problemi con il download di una foto')
                logger_download.warning(sys.exc_info())
                
                #print 'problemi con download foto'
                pass
            count=count+1
        except:
            ok=False


def download_auto_view(request,film_id,tipo='35mm'):
    elenco_link=MovieLink.objects.filter(tipo=tipo,movie_id=film_id)
    for link in elenco_link:
        #film=Movie.objects.get(id=link.movie.id)
        #print 'id: ' + str(link.movie.id)
        #print 'titolo : ' + film.titolo
        download_auto(link,tipo)
    
    
    parameters=get_default_parameter()
    parameters['res'] = 'ok'
    parameters['film_id'] = film_id
    parameters['tipo'] = tipo
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'download.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def download_auto(link,tipo='35mm'):
    persone=None
    result=None
    link_foto=None
    movie=link.movie
    logger_download.info('----------------------------------------------')
    logger_download.info('scarico le info del film ' + str(link.movie.id))
    if (tipo=='wikipedia') and (settings.USE_WIKIPEDIA==True):
        result,persone=get_info_wikipedia(link.link)
        
    if tipo=='35mm':
        result,persone,link_foto=get_info_35mm(link.link,0)
        download_foto(movie,link_foto,'locandina')
        
    if tipo=='mymovies':
        result,persone,link_foto=get_info_mymovies(link.link,0)
        download_foto(movie,link_foto)
    
    if tipo=='coming':
        result,persone,link_foto=get_info_comingsoon(link.link,0)
        
        download_foto(movie,link_foto)
        
        #print result
        
        
    save=0
    if result:
        logger_download.info(result)
        try:
            save_film_ext(movie,result)
            save=1
        except:
            logger_download.info(sys.exc_info())
            save=0
        
        #try:
        if tipo=='35mm':
            try:
                link_foto=get_link_foto_35mm(result['gallery_link'])
                download_foto(movie,link_foto)
            except:
                link_foto=None
            
        
    if persone:
        save_persone_ext(movie,persone)
    
    return(save)
# Create your views here.
def download(request,film_id,link,tipo='35mm'):
    film=Movie.objects.get(id=film_id)
    if tipo=='35mm':
        result,persone,link_foto=get_info_35mm(link)
        download_foto(film,link_foto,'locandina')
        result['tipo']=tipo
    if tipo=='imdb':
        result,persone=get_info_imdb(link)
        result['tipo']=tipo
    if tipo=='comingsoon':
        result,persone,link_foto=get_info_comingsoon(link)
        result['tipo']=tipo
    if tipo=='filmtv':
        result,link_foto=get_info_filmtv(link)
        result['tipo']=tipo
        #result=None
        persone=None
    
    if result:
        save_film_ext(film,result)
        #try:
        if tipo=='35mm':
            try:
                link_foto=get_link_foto_35mm(result['gallery_link'])
            except:
                link_foto=None
        download_foto(film,link_foto)
            
        #except:
            #print 'problemi con le foto'
        #pass
    if persone:
        save_persone_ext(film,persone)
    
    parameters=get_default_parameter()
    parameters['res'] = 'ok'
    parameters['film_id'] = film_id
    parameters['tipo'] = tipo
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'download.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))



def download_list(request,film_id,tipo='35mm',titolo=None):
    film=Movie.objects.get(id=film_id)

    #print film.titolo
    if tipo=='35mm':
        
            
        if titolo==None:
            res=trova_titoli_35mm(film.titolo)
        else:
            res=trova_titoli_35mm(titolo)
            
        try:
            movielink=MovieLink.object.get(movie=film,tipo=tipo)
        
            titolo=titoli_model()
            
            titolo.link=movielink.link.replace('http://film.35mm.it/','')
            titolo.titolo='<font color=\'red\'>GIA Presente</font>'
            titolo.anno=0
            res.append(titolo)
        except:
            pass
    if tipo=='comingsoon':
        if titolo==None:
            res=trova_titoli_comingsoon(film.titolo)
        else:
            res=trova_titoli_comingsoon(titolo)
    if tipo=='imdb':
        if titolo==None:
            res=trova_titoli_imdb(film.titolo)
        else:
            res=trova_titoli_imdb(titolo)
    
    if tipo=='filmtv':
        if titolo==None:
            res=trova_titoli_filmtv(film.titolo)
        else:
            res=trova_titoli_filmtv(titolo)
    
    parameters=get_default_parameter()
    
    parameters['res'] = res
    parameters['film_id'] = film_id
    parameters['tipo'] = tipo
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'download.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def gallery(request,movie_id):
    
    film=Movie.objects.get(id=movie_id)
    
    parameters=get_default_parameter()
    #parameters['generi_list'] = generi_list
    parameters['page_tipe'] = 'gallery'
    
    parameters['film'] = film
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def supporto(request,supporto_id):
    #generi_list=Genere.objects.all()
    
    film_list=get_film_list(0,'',supporto_id,'','')
    items=get_pagination_film(1,film_list)
    
    parameters=get_default_parameter()
    #parameters['generi_list'] = generi_list
    parameters['film_list'] = items
    parameters['page_tipe'] = 'supporto'
    #parameters['form'] = form
    parameters['genere']=0
    parameters['supporto'] = supporto_id
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def supporto_lista(request,supporto_id):
    #generi_list=Genere.objects.all()
    #generi_list,form=get_default()
    supporto=Supporti.objects.get(id=supporto_id)
    film_list=get_film_list(0,'',supporto_id,'','')
    #items=get_pagination_film(1,film_list)
    
    parameters=get_default_parameter()
    #parameters['generi_list'] = generi_list
    parameters['film_list'] = film_list
    parameters['page_tipe'] = 'supporto_lista'
    #parameters['form'] = form
    parameters['genere']=0
    parameters['supporto'] = supporto
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))




def client_detail(user_agent):
    #Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 
    #Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5
    client={}
    client['os']='na'
    client['os_version'] = 'na'
    client['browser']= 'na'
    client['browser_version']= 'na'
    client['allowed_preview'] = 'ogg'
    pos=user_agent.find('Android')
    if pos>0:
        pos2=user_agent.find(' ',pos)
        pos3=user_agent.find(';',pos2)
        client['os_version']=user_agent[pos+2:pos3]
        client['os']='Android'
        client['allowed_preview'] = 'mp4'
        
    if client['os']=='na':
    
        pos=user_agent.find('Linux')
        if pos>0:
            client['os']='Linux'
        
        pos=user_agent.find('Firefox')
        if pos>0:
            pos2=user_agent.find('/',pos)
            pos3=user_agent.find(' ',pos2)
            client['browser_version']=user_agent[pos2+1:pos3]
            client['browser']='Firefox'
        pos=user_agent.find('Chrome')
        if pos>0:
            pos2=user_agent.find('/',pos)
            pos3=user_agent.find(' ',pos2)
            client['browser_version']=user_agent[pos2+1:pos3]
            client['browser']='Chrome'
        
    
    return client

def scheda(request,film_id):
    
    client=client_detail(request.META['HTTP_USER_AGENT'])
    
    film=Movie.objects.get(id=film_id)
    filmlinks=MovieLink.objects.filter(movie=film)
    
    filmmedia_orig=MovieMedia.objects.filter(movie=film,tipo='orig')
    filmmedia_youtube=MovieMedia.objects.filter(movie=film,tipo='youtube')
    filmmedia_local=MovieMedia.objects.filter(movie=film,tipo='local')
    
    #generi_list,form=get_default()
    parameters=get_default_parameter()
    parameters=theme(parameters)
    
    parameters['film'] = film
    parameters['client'] = client
    parameters['user_agent'] = request.META['HTTP_USER_AGENT']
    parameters['filmlinks'] = filmlinks
    parameters['filmmedia_orig'] = filmmedia_orig
    parameters['filmmedia_youtube'] = filmmedia_youtube
    parameters['filmmedia_local'] = filmmedia_local
    #parameters['generi_list'] = generi_list
    parameters['page_tipe'] = 'scheda'
    #parameters['form'] = form
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))
   
def get_film_list(genere,titolo,supporto,attori,regia,anno=0):
    film_list=None
    
    if (titolo=='' and genere==0 and supporto==0 and attori==''  and regia=='' and anno==0):
        film_list=Movie.objects.all().order_by('-data_ins')
        
    if titolo!='':
        film_list=Movie.objects.filter(Q(titolo__icontains=titolo)| Q(titolo_originale__icontains=titolo))
            
    if genere>0:
        if film_list==None:
            film_list=Movie.objects.filter(genere__id=genere)
        else:
            film_list=film_list.filter(genere__id=genere)
            
    if supporto>0:
        if film_list==None:
            film_list=Movie.objects.filter(supporto__id=supporto).order_by('anno')
        else:
            film_list=film_list.filter(supporto__id=supporto)
            
    if attori!='':
        if film_list==None:
            film_list=Movie.objects.filter(attori__cognome=attori)
        else:
            film_list=film_list.filter(attori__cognome=attori)
            
    if regia!='':
        if film_list==None:
            film_list=Movie.objects.filter(regia__cognome=attori)
        else:
            film_list=film_list.filter(regia__cognome=attori)
    
    if anno!=0:
        if film_list==None:
            film_list=Movie.objects.filter(anno=anno)
        else:
            film_list=film_list.filter(anno=anno)
    return(film_list)

def get_pagination_film(page,film_list,size=10):
    
    paginator = Paginator(film_list, size)
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    return items

def index(request,genere=0,anno=0):
    film_list=None
    
    
    #print request.device
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            _genere = form.cleaned_data['genere']
            titolo = form.cleaned_data['titolo']
            supporto = form.cleaned_data['supporto']
            attori= form.cleaned_data['attori']
            regia=form.cleaned_data['regia']
            if _genere==0:
                _genere=genere
            else:
                genere=_genere
            film_list=get_film_list(_genere,titolo,supporto,attori,regia)
            
            #film_list=Movie.objects.filter(genere=genere)
            
        else:
            #print 'errata'
            #print form.errors
            pass
            
    else:
        #print 'no post'
        
        form = SearchForm()
        
        if genere!=0:
            film_list=get_film_list(genere,'',0,'','')
        elif anno!=0:
            film_list=get_film_list(0,'',0,'','',anno)
        else:
            film_list=get_film_list(0,'',0,'','')
            
    if film_list!=None:            
        items=get_pagination_film(1,film_list)
    else:
        items=None
    
    #print request.META['HTTP_USER_AGENT']

    
    parameters=get_default_parameter()
    #parameters['generi_list'] = generi_list
    parameters['page_tipe'] = 'home'
    parameters['form'] = form
    parameters['film_list'] = items
    parameters['genere']=genere
    parameters['supporto']=0
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def index_mobile(request,genere=0):
    film_list=None
    

    #print request.device
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            _genere = form.cleaned_data['genere']
            titolo = form.cleaned_data['titolo']
            supporto = form.cleaned_data['supporto']
            attori= form.cleaned_data['attori']
            regia=form.cleaned_data['regia']
            if _genere==0:
                _genere=genere
            else:
                genere=_genere
            film_list=get_film_list(_genere,titolo,supporto,attori,regia)
            
            #film_list=Movie.objects.filter(genere=genere)
            
        else:
            #print 'errata'
            #print form.errors
            pass
            
    else:
        #print 'no post'
        form = SearchForm()
        
    if genere!=0:
        if film_list==None:
            film_list=get_film_list(genere,'',0,'','')
            
    if film_list==None:
        film_list=get_film_list(0,'',0,'','')
    
    if film_list!=None:            
        items=get_pagination_film(1,film_list)
    else:
        items=None
    
    #print request.META['HTTP_USER_AGENT']

    
    parameters=get_default_parameter()
    #parameters['generi_list'] = generi_list
    parameters['page_tipe'] = 'home'
    parameters['form'] = form
    parameters['film_list'] = items
    parameters['genere']=genere
    parameters['supporto']=0
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home_mobile.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))