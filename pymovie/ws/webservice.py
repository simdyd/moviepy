from datetime import timedelta, date, time
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Context, loader, RequestContext
from django.utils import simplejson
from film.models import Movie, Supporti
from film.views import get_film_list,get_pagination_film
from persone.models import Persona
import datetime
import sys
import urllib

def get_movie_list_spalla(request):
    tipo=request.GET['tipo']
    objectid= request.GET['objectid']
    parameters={}
    if tipo=='R' or tipo=='A':
        if tipo=='R':
            movie_list=Movie.objects.filter(regia=objectid)
        if tipo=='A':
            movie_list=Movie.objects.filter(attori=objectid)
        persona=Persona.objects.get(id=objectid)
        parameters['persona']=persona
    if tipo=='Y':
        movie_list=Movie.objects.filter(anno=objectid)
        parameters['anno']=objectid
    if tipo=='S':
        parameters['supporto']=Supporti.objects.get(id=objectid)
        movie_list=Movie.objects.filter(supporto=objectid)
        
    
    #produzioneid = request.GET['att']
    
    parameters['movie_list']=movie_list
    
    t = loader.get_template('block/spalla_elenco_film.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def get_movie_detail(request):
    parameters={}
    filmid=int(request.GET['filmid'])
    movie=Movie.objects.get(id=filmid)
    parameters['film']=movie
    t = loader.get_template('block/spalla_film_detail.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def change_list_page(request):
    parameters={}
    try:
        genere= int(request.GET['genere'])
    except:
        genere=0
    try:
        supporto= int(request.GET['supporto'])
    except:
        supporto=0
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        no_thumbnail = int(request.GET['no_thumbnail'])
    except:
        no_thumbnail = 0   
    
    try:
        no_video= int(request.GET['no_video'])
    except:
        no_video=0
    
    
        
    if no_thumbnail==0 and no_video==0:
        film_list=get_film_list(genere,'',supporto,'','')
    elif no_thumbnail==1:
        film_list=Movie.objects.filter(foto=None)
    elif no_video==1:
        film_list=Movie.objects.filter(video_file=None)
        
    items=get_pagination_film(page,film_list)
    parameters['film_list']= items
    parameters['genere']= genere
    parameters['supporto']=supporto
    parameters['no_thumbnail']=no_thumbnail
    parameters['no_video']=no_video

    
    t = loader.get_template('film/elenco_img.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))