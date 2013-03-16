from download.download import *
from film.models import *

#919 next

def save_movie_ext(link,id,type='35'):
    film=Movie.objects.get(id=id)
    result,persone=get_info_35mm(link)
    if result:
        film.titolo=result['titolo']
        film.titolo_originale=result['titolo_originale']
        film.durata=result['durata']
        film.anno=result['anno']
        #result['uscita']
        film.paese=result['nazione']
    
        genere=Genere.objects.get(nome=result['genere'])
        print 'id genere ' + str(genere.id)
        film.genere=genere
        film.trama=result['descrizione']
        film.save()

id_movie=932

film=Movie.objects.get(id=id_movie)
#trova_titoli_35mm(film.titolo)

save_movie_ext('http://film.35mm.it/watchmen-2009.html',id_movie)


