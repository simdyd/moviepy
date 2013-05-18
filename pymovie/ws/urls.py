from django.conf.urls.defaults import *

urlpatterns = patterns('ws',
    (r'get_movie_list_spalla/$', 'webservice.get_movie_list_spalla'),
    (r'change_list_page/$','webservice.change_list_page'),
    (r'get_movie_detail/$','webservice.get_movie_detail'),
    (r'mobile/genere_list/$','webservice.get_mobile_genere_list'),
    (r'mobile/film_list_genere/(?P<genere>[^/]+)/$','webservice.get_mobile_film_list_genere'),
    (r'mobile/get_film_img/(?P<movie_id>\d+)/$','webservice.get_mobile_film_img'),
    (r'mobile/get_film_trama/(?P<movie_id>\d+)/$','webservice.get_mobile_film_trama'),
    )
