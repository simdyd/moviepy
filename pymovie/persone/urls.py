from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('persone',
     (r'scheda/(?P<persona_id>\d+)/$', 'views.scheda'),
     (r'elenco/$', 'views.elenco_persone'),
     (r'ricerca/$', 'views.ricerca_persone'),
     (r'elenco/(?P<professione_id>\d+)/$', 'views.elenco_persone'),
     (r'download/(?P<tipo>[^/]+)/(?P<persona_id>\d+)/$', 'views.view_download_pers'),
)