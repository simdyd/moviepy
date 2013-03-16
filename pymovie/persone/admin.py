from persone.models import Persona, Professioni, PersonaLink
from django.contrib import admin

class PersonaLinkInLine(admin.TabularInline):
    model = PersonaLink
    extra=1

class PersonaAdmin(admin.ModelAdmin):
    search_fields = ['nome','cognome']
    list_display = ('nome','cognome','sesso','data_nascita','luogo_nascita',"thumb")
    #raw_id_fields = ('supporto','foto','regia',)
    save_as = True
    raw_id_fields = ('foto',)
    list_filter = [ 'professione','sesso']
    inlines = [PersonaLinkInLine,]
    filter_vertical = ('foto',)
    
admin.site.register(Persona,PersonaAdmin)

admin.site.register(Professioni)

admin.site.register(PersonaLink)

