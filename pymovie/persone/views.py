from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from download.download import *


from film.models import Movie
from film.views import get_default_parameter
from media.models import Photo
from persone.forms import SearchPersonaForm
from persone.models import *
import Image
import datetime
import logging
import os
import sys
import urllib

if settings.USE_WIKIPEDIA==True:
    from download.download_wikipedia import get_pers_wikipedia

# Create your views here.
logger_download = logging.getLogger('movie_download')

def ricerca_persone(request):
    parameters=get_default_parameter()
    professioni_list=Professioni.objects.all().order_by('professione')
    elenco_persone=None
    if request.method == 'POST':
        form_persone = SearchPersonaForm(request.POST)
        if form_persone.is_valid():
            nome = form_persone.cleaned_data['nome']
            professione = form_persone.cleaned_data['professione']
            elenco_persone=Persona.objects.filter(Q(nome__icontains=nome) | Q(cognome__icontains=nome)).filter(professione=professione).order_by('cognome','nome')
        
        
        
    paginator = Paginator(elenco_persone, 20) 

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        persone = paginator.page(page)
    except (EmptyPage, InvalidPage):
        persone = paginator.page(paginator.num_pages)


    
    #parameters['generi_list'] = generi_list
    parameters['professioni_list'] = professioni_list
    parameters['page_tipe'] = 'elenco_persone'
    parameters['persone'] = persone
    #parameters['form'] = form
    parameters['form_persone'] = SearchPersonaForm ()
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


def elenco_persone(request,professione_id=0):
    #generi_list,form=get_default()
    parameters=get_default_parameter()
    professioni_list=Professioni.objects.all().order_by('professione')
    if professione_id==0:
        elenco_persone=Persona.objects.all().order_by('cognome','nome')
    else:
        elenco_persone=Persona.objects.filter(professione__id=professione_id).order_by('cognome','nome')
        
        
    paginator = Paginator(elenco_persone, 20) 

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        persone = paginator.page(page)
    except (EmptyPage, InvalidPage):
        persone = paginator.page(paginator.num_pages)


    #parameters={}
    #parameters['generi_list'] = generi_list
    parameters['professioni_list'] = professioni_list
    parameters['page_tipe'] = 'elenco_persone'
    parameters['persone'] = persone
    #parameters['form'] = form
    parameters['form_persone'] = SearchPersonaForm ()
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def scheda(request,persona_id):
    persona=Persona.objects.get(id=persona_id)
    #generi_list,form=get_default()
    parameters=get_default_parameter()
    filmografia=Movie.objects.filter(attori=persona).order_by('anno')
    elenco_link=PersonaLink.objects.filter(persona=persona)
    #parameters=theme()
    #parameters={}
    parameters['persona'] = persona
    parameters['elenco_link'] = elenco_link
    parameters['filmografia'] = filmografia
    #parameters['generi_list'] = generi_list
    parameters['page_tipe'] = 'scheda_persona'
    #parameters['form'] = form
    parameters['form_persone'] = SearchPersonaForm ()
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def download_multiple_foto_pers(persona,foto_link):
    count=0
    ok=True
    while ok==True:
        try:
            link=foto_link[count]
            
        except:
            logger_download.warning('error download foto persona ' + link)
            ok=False
        if ok==True:   
            download_foto_pers(persona,link)
            count=count+1
            
        
def download_foto_pers(persona,link_foto):
   
    ok=True
    now=datetime.datetime.now()
    new_file_dir = os.path.dirname(settings.MEDIA_ROOT+now.strftime("%Y"+os.sep+"%m"+os.sep))
    if not os.path.exists(new_file_dir):
        os.makedirs(new_file_dir)
    
    try:
        link=link_foto
        pos=link.rfind('/')
        nome_foto=link[pos+1:]
        try:
            nome_foto=nome_foto.replace('%20','_')
            name = now.strftime("%Y"+os.sep+"%m"+os.sep) + "pers" + str(persona.id) + nome_foto
            #print name
            try:
                image = urllib.URLopener()
                image.retrieve(link,settings.MEDIA_ROOT + name)
            except:
                logger_download.warning('impossibile fare download')
                logger_download.warning(link)
                image=None
            if image!=None:
                try:
                    img = Photo.objects.get(image=name)
                except:    
                    img = Photo()
                    img.name = nome_foto
                    img.image = name
                    img.caption=persona.nome + ' ' + persona.cognome 
                    img.upload_date = datetime.datetime.now()
                    img.publish_date = datetime.datetime.now()                    
                    img.save()
            
                    persona.foto.add(img)
                    persona.save()
        except:
            
            logger_download.warning('problemi con download foto')
            logger_download.warning(sys.exc_info())
            
            
    except:
        logger_download.warning(sys.exc_info())
        ok=False

def view_download_pers(request,persona_id,tipo='35mm'):
    elenco_link=PersonaLink.objects.filter(persona__id=persona_id,tipo_link=tipo)
    for personalink in elenco_link:
        parameters=download_pers(personalink)
    t = loader.get_template(settings.SITE_TEMPLATE_PAGES_BASE_PATH +  'download_pers.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def download_pers(personalink):
    persona=Persona.objects.get(id=personalink.persona.id)
    parameters={}
    parameters['res'] = 'ko'
    parameters['persona_id'] = persona.id
    #parameters['tipo'] = tipo
    
    if (personalink.link!=None):
        logger_download.info('Scarico i dati della persona ' + str(persona.id))
        result=None
        if (personalink.tipo_link=='35mm'):
            result=get_pers_35mm(personalink.link)
        if (personalink.tipo_link=='wikipedia') and (settings.USE_WIKIPEDIA==True):
            
            result=get_pers_wikipedia(personalink.link)
            
        if (result!=None):
            logger_download.info('Scarico il link ' + personalink.link)
            persona.sesso=result['sesso']
            #print persona.sesso
            if result['luogo_nascita']!=None:
                persona.luogo_nascita=result['luogo_nascita']
            if result['biografia']!=None:
                persona.biografia=result['biografia']
            try:
                if result['data_nascita']!=None:
                    persona.data_nascita=datetime.datetime.strptime(result['data_nascita'], '%d/%m/%Y')
            except:
                pass
            personalink.download=1
            try:
                personalink.save()
            except:
                logger_download.warning(sys.exc_info())
            try:
                persona.save()
            except:
                logger_download.warning(sys.exc_info())
            
            
            if result['link_foto']!=None:
                download_foto_pers(persona,result['link_foto'])
            #scarico anche una eventuale gallery
            if (personalink.tipo_link=='35mm'):
                linkgallery=personalink.link.replace('.html','/foto.html')
                logger_download.info(linkgallery)
                link_foto=get_link_foto_pers_35mm(linkgallery)
                download_multiple_foto_pers(persona,link_foto)
                
            parameters['res'] = 'ok'
        else:
            logger_download.warning('non previsto il download delle persone per il tipo ' + personalink.tipo_link)
    return (parameters)
    