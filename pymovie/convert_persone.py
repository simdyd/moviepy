from django.conf import settings

from persone.models import Professioni, Persona
from film.models import Movie,persone_old


elenco=persone_old.objects.all()

for riga in elenco:
    #print movie.old_supporto
    #print riga.text
    if riga.text!='':
        persone=riga.text.split(',')
        for persona in persone:
            persona=persona.strip()
            pos=persona.find('(')
            if pos!=-1:
                pos2=persona.find(')')
                #print str(pos) + '    ' + str(pos2)
                parte=persona[pos:pos2]
                persona=persona[0:pos]
            
            try:
                part=str(persona).split(' ')
                xxx=0
                cognome=''
                for parte in part:
                    if xxx==0:
                        if parte!='':
                            nome=parte.strip()
                            xxx=xxx+1
                    else:    
                        if parte!='':
                            cognome=cognome+ ' ' + parte
                            xxx=xxx+1
            except:
                nome=persona
                cognome=''
            try:
                persona_obj=Persona.objects.get(nome=nome,cognome=cognome)
            except:
                persona_obj=Persona()
                
                persona_obj.nome=nome
                persona_obj.cognome=cognome
                try:
                    persona_obj.save()
                except:
                    print 'Impossibile Salvare ' + nome + ' '+ cognome.strip() 
            
            if riga.professione=='ATT':
                try:
                    persona_obj.professione.add(1)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.attori.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass
                
            if riga.professione=='REG':
                try:
                    persona_obj.professione.add(2)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.regia.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass
            
            if riga.professione=='SCE':
                try:
                    persona_obj.professione.add(3)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.sceneggiatura.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass
                
            if riga.professione=='FOT':
                try:
                    persona_obj.professione.add(4)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.fotografia.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass
            
            if riga.professione=='MUS':
                try:
                    persona_obj.professione.add(5)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.fotografia.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass                
            
            if riga.professione=='PRO':
                try:
                    persona_obj.professione.add(6)
                    persona_obj.save()
                    try:
                        film=Movie.objects.get(id=riga.film_id)
                        film.fotografia.add(persona_obj)
                    except:
                        print 'impossibile trovare il film'
                except:
                    pass
                
            film.save()
            
        print "=============================================================="