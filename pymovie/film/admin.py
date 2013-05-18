from film.models import Formati,Genere,Supporti,MovieFoto,Movie,MovieLink, MovieMedia

from persone.models import Persona
from media.models import Photo
from django.contrib import admin

admin.site.register(Formati)

admin.site.register(Genere)

class MovieLinkAdmin(admin.ModelAdmin):
    list_display = ('id','movie','tipo','download',)
    save_as = True
    save_on_top = True
    list_filter = [ 'tipo','download']
    
admin.site.register(MovieLink,MovieLinkAdmin)

admin.site.register(MovieMedia)

class SupportoInLine(admin.TabularInline):
    #fields = ("supporto__nome","supporto__gruppo")
    model = Movie.supporto.through
    raw_id_fields = ("supporti",)
    extra=1
    
class AttoriInLine(admin.TabularInline):
    model = Movie.attori.through
    
    #readonly_fields=( "persona__admin_image",)
    #fields = ('persona','persona__admin_image')
    raw_id_fields = ("persona",)
    extra=1

class RegiaInLine(admin.TabularInline):
    model = Movie.regia.through
    raw_id_fields = ("persona",)
    extra=1
    
class MovieLinkInLine(admin.TabularInline):
    model = MovieLink
    extra=1

class MovieMediaInLine(admin.TabularInline):
    model = MovieMedia
    extra=1
    


class MovieFotoInLine(admin.TabularInline):
    raw_id_fields = ('foto',)
    #list_display = ('foto', 'admin_image')
    readonly_fields=( 'admin_image',)
    fields = ('foto','ordine','tipo','admin_image')
    model = MovieFoto
    extra=1
    
class MovieFotoAdmin(admin.ModelAdmin):
    search_fields = ['movie__titolo','movie__titolo_originale',]
    raw_id_fields = ('movie','foto')
    list_filter = [ 'tipo',]
    list_display = ('id','movie','ordine','foto','tipo','admin_image')
    save_as = True
    save_on_top = True
    
    
admin.site.register(MovieFoto, MovieFotoAdmin)


class MovieAdmin(admin.ModelAdmin):
    search_fields = ['titolo','titolo_originale','id',]
    list_display = ('id','titolo','anno',)
    raw_id_fields = ('regia','fotografia','sceneggiatura','musica','produttore','supporto')
    fieldsets=(
               (None,{
                      'fields': ('titolo', 'titolo_originale', 'trama', 'recensione','genere','durata','anno','formato')
                      }),
               ('Dati Video',{
                              'classes': ('collapse',),
                              'fields': ('video_file','file_durata','file_bitrate','file_audio','file_video','qual_audio','qual_video')
                              })
               )
    exclude = ('attori','supporto')

    inlines = [
        MovieFotoInLine,
        MovieMediaInLine,
        MovieLinkInLine,
        SupportoInLine,
        AttoriInLine,
        RegiaInLine,
        #PhotoInLine,
    ]

    save_as = True
    save_on_top = True
    list_filter = [ 'genere','supporto']
    
admin.site.register(Movie, MovieAdmin)


class SupportiAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ['nome','gruppo']
    list_filter = ['gruppo',]
    save_as = True
    save_on_top = True
    
admin.site.register(Supporti,SupportiAdmin)

    


