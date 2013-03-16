from serietv.models import Serietv, Episodi, Supporti
from django.contrib import admin
from link.admin import LinkInlines

class SerietvAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    save_on_top=True
    save_as = True
    inlines = [LinkInlines,]


admin.site.register(Serietv,SerietvAdmin)

class SupportiAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome','box','posizione')
    list_filter = ['box']
    save_on_top=True
    save_as = True
    raw_id_fields = ('episodi',)

admin.site.register(Supporti,SupportiAdmin)

class EpisodiAdmin(admin.ModelAdmin):
    search_fields = ['titolo']
    list_display = ('titolo','stagione','episodio','serietv',"thumb")
    save_on_top=True
    save_as = True
    inlines = [LinkInlines,]
    raw_id_fields = ('foto',)
    list_filter = [ 'stagione','serietv',]

admin.site.register(Episodi,EpisodiAdmin)