from django.conf import settings
from film.models import *
from film.views import *

if settings.USE_WIKIPEDIA==True:
    elenco_link=MovieLink.objects.filter(tipo='wikipedia',download=False)
    for link in elenco_link:
        #film=Movie.objects.get(id=link.movie.id)
        print 'id: ' + str(link.movie.id)
        #print 'titolo : ' + film.titolo
        download_auto(link,'wikipedia')

elenco_link=MovieLink.objects.filter(tipo='35mm',download=False)
for link in elenco_link:
    #film=Movie.objects.get(id=link.movie.id)
    print 'id: ' + str(link.movie.id)
    #print 'titolo : ' + film.titolo
    download_auto(link,'35mm')

elenco_link=MovieLink.objects.filter(tipo='mymovies',download=False)
#elenco_link=MovieLink.objects.filter(movie__id=1893)
for link in elenco_link:
#link = elenco_link[0]
    film=Movie.objects.get(id=link.movie.id)
    print 'id: ' + str(link.movie.id)
    #print 'titolo : ' + film.titolo
    download_auto(link,'mymovies')
    