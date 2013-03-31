from django.conf import settings

from film.models import Movie
import os
import sys

root=settings.FOLDER_VIDEO
link_folder='/media/Storage_1/Film/per_sezioni/'
link_folder_year='/media/Storage_1/Film/per_anno/'
link_folder_supporto='/media/Storage_1/Film/supporti/'
#Controllo presenza anteprime.
lista_cartelle=root.split(',')
for cartella in lista_cartelle:
    list_files = []
    list_files = os.listdir(cartella)

    for file in list_files:
        try:
            #print file
            #file=unicode(file)
            pos=file.find('.')
            if pos:
                num=int(file[0:pos])
                try:
                    movie=Movie.objects.get(id=num)
                    #creo albero per genere...
                    
                    if movie.genere!=None:
                        try:
                            #print cartella+movie.genere.nome
                            os.mkdir(link_folder+movie.genere.nome)
                            os.chmod(link_folder+movie.genere.nome, 0777)
                        except:
                            pass
                        
                        #print cartella+file
                        try:
                            if movie.anno!=None and movie.anno!=0:
                                os.symlink(cartella+file,link_folder+movie.genere.nome+'/'+str(movie.anno)+'.'+file)
                                os.chmod(link_folder+movie.genere.nome+'/'+str(movie.anno)+'.'+file, 0777)
                            else:
                                os.symlink(cartella+file,link_folder+movie.genere.nome+'/'+file)
                                os.chmod(link_folder+movie.genere.nome+'/'+file, 0777)
                        except:
                            print '----------genere---------------'
                            print sys.exc_info()
                            print file
                            print '--------------------------'
                            pass
                    #creo albero per anno...
                    if movie.anno!=None and movie.anno!=0:
                        try:
                            #print cartella+movie.genere.nome
                            os.mkdir(link_folder_year+str(movie.anno))
                            os.chmod(link_folder_year+str(movie.anno), 0777)
                        except:
                            #print sys.exc_info()[0]
                            pass
                        try:
                            if movie.genere!='':
                                os.symlink(cartella+file,link_folder_year+str(movie.anno)+'/'+movie.genere.nome+'.'+file)
                                os.chmod(link_folder_year+str(movie.anno)+'/'+movie.genere.nome+'.'+file, 0777)
                            else: 
                                os.symlink(cartella+file,link_folder_year+str(movie.anno)+'/'+file)
                                os.chmod(link_folder_year+str(movie.anno)+'/'+file, 0777)
                        except:
                            print '----------------anno ----------------'
                            print sys.exc_info()
                            print file
                            print '-------------------------------------'
                            pass
                    #creo albero per supporto...
                    elenco_supporti=movie.get_supporti()
                    
                    if elenco_supporti!=None:
                        for supporto in elenco_supporti:
                            try:
                                os.mkdir(link_folder_supporto+str(supporto.gruppo)+'/')
                                os.chmod(link_folder_supporto+str(supporto.gruppo)+'/', 0777)
                            except:
                                pass
                            try:
                                os.mkdir(link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome))
                                os.chmod(link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome), 0777)
                            except:
                                pass
                                #print 'Errore creazione cartella supporto ' + str(supporto.nome)
                                #print sys.exc_info()[0]
                            try:
                                if movie.anno!=None and movie.anno!=0:
                                    os.symlink(cartella+file,link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome)+'/'+str(movie.anno)+'.'+file)
                                    os.chmod(link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome)+'/'+str(movie.anno)+'.'+file, 0777)
                                else:
                                    os.symlink(cartella+file,link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome)+'/'+file)
                                    os.chmod(link_folder_supporto+str(supporto.gruppo)+'/'+str(supporto.nome)+'/'+file, 0777)
                            except:
                                pass
                                #print 'Errore creazione link supporto ' + str(supporto.nome)
                                print sys.exc_info()
                                
                except:
                    print 'id : ' + str(num)
                    print 'file ' + file
                    print sys.exc_info()[0]
                    
                
        except:
            pass
            print 'problemi con l\'id'
            print file

