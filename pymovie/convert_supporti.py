from django.conf import settings


from film.models import Movie,Supporti


elenco=Movie.objects.all()

for movie in elenco:
    #print movie.old_supporto
    tmp=movie.old_supporto.split(',')
    for supp in tmp:
        if supp=='':
            supp='na'
        try:
            supporto=Supporti.objects.get(nome=supp)
        except:
            supporto=Supporti()
            supporto.nome=supp
            supporto.save()
            
        movie.supporto.add(supporto)
        movie.save()
        print supp