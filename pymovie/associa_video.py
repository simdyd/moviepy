from django.conf import settings

from film.models import Movie,MovieMedia
from film.views import ricava_parametri_video
from media.models import Photo
import os
import sys

##controllo presenza foto
#foto_list=Photo.objects.all()
#count_good=0
#count_bad=0
#for foto in foto_list:
#    try:
#        s=os.stat(settings.MEDIA_ROOT+str(foto.image))
#        count_good+=1
#    except:
#        print foto.image
#        foto.delete()
#        count_bad+=1
#print 'good ' + str(count_good)
#print 'bad ' + str(count_bad)


root=settings.FOLDER_VIDEO



##Controllo Presenza File...
movie_list=Movie.objects.exclude(video_file=None)
for movie in movie_list:
     try:
         s = os.stat(movie.video_file)
     except:
         movie.video_file=None
         movie.save()
 

video_media_list=MovieMedia.objects.filter(tipo='orig')
for video_media in video_media_list:
    try:
        s= os.stat(video_media.file)
    except:
        video_media.delete()
        
##Controllo presenza anteprime.
#movie_list=Movie.objects.filter(preview=1)
#for movie in movie_list:
#    flvfilename = "%s.flv" % movie.id
#    targetfile = "%s%s" % (settings.PREVIEW_ROOT , flvfilename)
#    try:
#        s = os.stat(targetfile)
#        fsize = s.st_size
#        if (fsize == 0):
#            os.remove(targetfile)
#            movie.preview=0
#            movie.video_file=None
#            movie.save()
#    except:
#        #file non esiste
#        movie.preview=0
#        movie.video_file=None
#        movie.save()
        
lista_cartelle=root.split(',')
size=len(lista_cartelle)

for cartella in lista_cartelle:
    try:
        list_files = []
        list_files = os.listdir(cartella)
        print 'Sto processando la cartella ' + cartella
        for file in list_files:
            try:
                #print file
                pos=file.find('.')
                if pos:
                    num=int(file[0:pos])
                    try:
                        
                        movie = Movie.objects.get(id=num)
                        print num
                        full_file_name = cartella + file
                        file_url= full_file_name.replace ('/media/','/media_movie/orig/')
                        try:
                            movie_media=MovieMedia.objects.get(file=full_file_name,movie=movie,tipo='orig')
                        except:
                            movie_media=MovieMedia()
                            movie_media.file=full_file_name
                            movie_media.file_url=file_url
                            movie_media.movie=movie
                            movie_media.tipo='orig'
                            try:
                                basename, extension = os.path.splitext(full_file_name)
                                extension=extension.replace('.','')
                                movie_media.file_type=extension
                            except:
                                print 'problemi con extension'
                            try:
                                movie_media.file_size=os.path.getsize(full_file_name)
                            except:
                                print 'problemi con la dimensione'
                            try:
                                movie_media.save()
                            except:
                                print 'Problemi salvataggio media' 
                            try:
                                ricava_parametri_video(movie)
                            except:
                                print 'Problemi con i parametri del video'
                            #print 'check 1'
                            
                        if (movie.video_file==None):
                            
                            print 'Trovato file con id ' + str(num)
                            
                                
                            movie.video_file=full_file_name
                            movie.save()
                            
                            movie.ricava_parametri_video()
                        #Verifica e nel caso crea le anteprime
                        #movie.create_preview('mp4')
                        #movie.create_preview('ogg')
                    except:
                        print sys.exc_info()[0]
                        print 'video non trovato ' + str(num)
            except:
                pass
                print 'problemi con l\'id ' + file
    except:
        pass
        print sys.exc_info()[0]
        print 'Problemi con la cartella ' + cartella


#movie_list=Movie.objects.exclude(video_file=None)
#for movie in movie_list:
#    try:
#        moviemedia_list=MovieMedia.objects.get(movie=movie,tipo='local')
#    except MovieMedia.DoesNotExist:
#        print 'Processo il film ' + str(movie.id)
#        movie.save()
        
