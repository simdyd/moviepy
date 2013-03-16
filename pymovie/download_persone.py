from persone.models import *
from persone.views import *

elenco_persone=PersonaLink.objects.filter(download=0)
#elenco_persone=Persona.objects.exclude(link='').filter()

for personalink in elenco_persone:
    print 'id:  ' + str(personalink.persona.id)
    if personalink.link!='':
        
        download_pers(personalink)
        
    #persona.download=1
    #persona.save()