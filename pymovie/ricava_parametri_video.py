from django.conf import settings

from film.models import Movie
import os
import sys
movie_list=Movie.objects.filter(preview=1)
for movie in movie_list:
    try:
        movie.ricava_parametri_video()
    except:
        print 'Problemi con il film ' + str(movie.id)