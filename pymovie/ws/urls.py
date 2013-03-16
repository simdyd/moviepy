from django.conf.urls.defaults import *

urlpatterns = patterns('ws',
    (r'get_movie_list_spalla/$', 'webservice.get_movie_list_spalla'),
    (r'change_list_page/$','webservice.change_list_page'),
    (r'get_movie_detail/$','webservice.get_movie_detail'),
    )