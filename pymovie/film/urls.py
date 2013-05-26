from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('film',
     (r'^$', 'views.index'),
     (r'dashboard/$', 'views.dashboard'),
     (r'mobile/$', 'views.index_mobile'),
     (r'mobile/genere/(?P<genere>[^/]+)/$', 'views.index_mobile'),
     
     (r'genere/(?P<genere>[^/]+)/$', 'views.index'),
     (r'anno/(?P<anno>[^/]+)/$', 'views.index'),
     (r'no_thumbnail/$', 'views.get_film_senza_thumbnail'),
     (r'no_loca/$', 'views.get_film_senza_locandine'),
     (r'no_video/$', 'views.get_film_senza_video'),
     (r'scheda/(?P<film_id>\d+)/$', 'views.scheda'),
     (r'download/(?P<tipo>[^/]+)/(?P<film_id>\d+)/$', 'views.download_auto_view'),
     (r'download/(?P<tipo>[^/]+)/(?P<film_id>\d+)/(?P<link>[^/]+)/$', 'views.download'),
     (r'supporto/(?P<supporto_id>\d+)/$', 'views.supporto'),
     (r'supporto_lista/(?P<supporto_id>\d+)/$', 'views.supporto_lista'),
     (r'supporto_pdf/(?P<supporto_id>\d+)/$', 'views.supporto_pdf'),
     (r'gallery/(?P<movie_id>\d+)/$', 'views.gallery'),
)