from django.conf import settings


from film.models import Movie,Supporti,foto_old
import os
import Image
from media.models import Photo

old_root='/var/www/html/movie/images/'
#new_file_dir = os.path.dirname(settings.MEDIA_ROOT+datetime.datetime.now().strftime("%Y"+os.sep+"%m"+os.sep))

elenco_foto=foto_old.objects.all()

for foto in elenco_foto:
    source_file_dir=old_root+str(foto.film.id)+'/'+foto.nome_file
    if os.path.exists(source_file_dir):
        #print 'esiste ' + foto.nome_file
        film=Movie.objects.get(id=foto.film.id)
        new_file_dir = os.path.dirname(settings.MEDIA_ROOT+film.data_ins.strftime("%Y"+os.sep+"%m"+os.sep))
        #print new_file_dir
        if not os.path.exists(new_file_dir):
            os.makedirs(new_file_dir)
        
        name = film.data_ins.strftime("%Y"+os.sep+"%m"+os.sep) + str(film.id) + foto.nome_file
        try: 
            image = Image.open(source_file_dir)
            image = image.save(settings.MEDIA_ROOT + name)
            try:
                img = Photo.objects.get(image=name)
            except:    
                img = Photo()
                img.name = foto.nome_file
                img.image=name
                img.upload_date = film.data_ins
                img.publish_date = film.data_ins
                img.save()
        
                film.foto.add(img)
                film.save()
        except:
            print 'impossibile salvare immagine'
        #print film.titolo
        #foto=Photo()
    else:
        print 'non trovato ' + old_root+str(foto.film.id)+'/'+foto.nome_file