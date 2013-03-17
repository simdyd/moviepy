from django.conf import settings
from django.db import models
from persone.models import Persona
from media.models import Photo

from datetime import datetime
import commands
import os,sys
# Create your models here.
class Formati(models.Model):
    nome= models.CharField(verbose_name = "nome",max_length=20)
    
    def __unicode__(self):
        return self.nome
    
class Genere(models.Model):
    nome= models.CharField(verbose_name = "nome",max_length=20)
    
    def __unicode__(self):
        return self.nome
    
class Supporti(models.Model):
    nome= models.CharField(verbose_name = "nome",max_length=40)
    gruppo= models.CharField(verbose_name = "gruppo",max_length=20)
    def __unicode__(self):
        return self.nome





class Movie(models.Model):
    titolo = models.CharField(verbose_name = "Titolo",max_length=100)
    titolo_originale = models.CharField(verbose_name = "Titolo Originale",max_length=100,blank=True, null=True)
    formato = models.ForeignKey(Formati,verbose_name="Formato",blank=True,null=True)
    trama = models.TextField(verbose_name = "Trama",blank=True,null=True)
    recensione = models.TextField(verbose_name = "Recensione",blank=True,null=True)
    
    genere = models.ForeignKey(Genere,verbose_name="Genere",blank=True,null=True)
    durata = models.CharField(verbose_name = "Durata",max_length=30,blank=True,null=True)
    anno = models.IntegerField(verbose_name="anno",blank=True,null=True)
    attori = models.ManyToManyField(Persona,verbose_name="Attori",related_name='attori', blank=True, null=True, limit_choices_to = {'professione__short_id':  'ATT'})
    #cast = models.ManyToManyField(Persona,verbose_name="Cast",related_name='cast',  blank=True, null=True)
    regia = models.ManyToManyField(Persona,verbose_name="Regia",related_name='regia', blank=True, null=True, limit_choices_to = {'professione__short_id':  'REG'})
    supporto = models.ManyToManyField(Supporti,blank=True,null=True,related_name='supporto')
    #old_supporto = models.CharField(verbose_name = "old supporto",max_length=100,blank=True,null=True)
    sceneggiatura = models.ManyToManyField(Persona,verbose_name="Sceneggiatura",related_name='sceneggiatura', blank=True, null=True, limit_choices_to = {'professione__short_id':  'SCE'})
    fotografia = models.ManyToManyField(Persona,verbose_name="Fotografia",related_name='fotografia', blank=True, null=True, limit_choices_to = {'professione__short_id':  'FOT'})
    studio = models.CharField(verbose_name="Studio",max_length=50, blank=True, null=True)
    musica = models.ManyToManyField(Persona,verbose_name="Musica",related_name='musica', blank=True, null=True, limit_choices_to = {'professione__short_id':  'MUS'})
    produttore = models.ManyToManyField(Persona,verbose_name="Produttore",related_name='produttore', blank=True, null=True, limit_choices_to = {'professione__short_id':  'PRO'})
    #foto = models.ManyToManyField(Photo,verbose_name="Photo", blank=True, null=True)
    qual_audio =models.IntegerField(verbose_name="qual_audio",blank=True,null=True)
    qual_video =models.IntegerField(verbose_name="qual_video",blank=True,null=True)
    data_ins=models.DateTimeField('data Inserimento',blank=True,null=True,default=datetime.now)
    data_mod=models.DateTimeField('data Modifica',blank=True,null=True,default=datetime.now)
    paese = models.CharField(verbose_name = "Paese",max_length=100,blank=True,null=True)
    #link = models.CharField(verbose_name = "link", max_length=100,blank=True,null=True)
    
    video_file=models.CharField(verbose_name='video file', max_length=255,blank=True,null=True)
    file_durata=models.CharField(verbose_name='file durata', max_length=255,blank=True,null=True)
    file_bitrate=models.CharField(verbose_name='file bitrate', max_length=255,blank=True,null=True)
    file_audio=models.CharField(verbose_name='file dettagli audio', max_length=255,blank=True,null=True)
    file_video=models.CharField(verbose_name='file_dettagli_video', max_length=255,blank=True,null=True)
    
    #download =models.IntegerField(verbose_name="download",blank=True,null=True,default=0)
    
    
    def __unicode__(self):
        return self.titolo
    
    class Meta:
        ordering = ('-anno', 'titolo')

    def thumb(self):
        tmp=self.get_photo()
        try:
            foto=tmp[0]
        except:
            foto=None
        if foto!=None:
            return '<a href="%s"><img width="150" src="%s" /></a>' % (foto.getMediumUrl(), foto.getLowUrl())
        else:
            return '<img width="150" src="grafica/noimage.jpg">'
            #return '<img width="150" src="'+ settings.MEDIA_URL_SITE_REPOSITORY+ 'grafica/noimage.jpg">'
        
    thumb.allow_tags = True
    
    def has_photo(self):
        temp=MovieFoto.objects.filter(movie=self)
        tmp=len(temp)
        #print tmp
        if tmp>0:    
            return 1
        else:
            return 0
    
    def get_thumbnail(self):
        try:
            #result=self.foto.all()[0]
            tmp=MovieFoto.objects.filter(movie=self).order_by('ordine')[0]
            result=tmp.foto
        except:
            result=None
        return result
    
    def get_photo(self):
        #foto=self.foto.all()
        #print 'ppp' + self.foto[1].name
        list=[]
        for tmp in MovieFoto.objects.filter(movie=self).order_by('ordine'):
            list.append(tmp.foto)
        
        return list 
        #return self.foto.all()
    
    def get_musica(self):
        return self.musica.all().order_by('cognome')
    
    def get_produttori(self):
        return self.produttore.all().order_by('cognome')
    
    def get_fotografi(self):
        return self.fotografia.all().order_by('cognome')
    
    def get_sceneggiatori(self):
        return self.sceneggiatura.all().order_by('cognome')
    
    def get_attori(self):
        return self.attori.all().order_by('cognome')
    
    def get_regista(self):
        return self.regia.all().order_by('cognome')
    
    def get_supporti(self):
        return self.supporto.all().order_by('nome')
    
    def create_preview(self,preview_kind=settings.PREVIEW_KIND):
        
        if ((self.video_file!='') and (self.video_file!=None)):
            filename = self.video_file
            fout = file(settings.LOG_ROOT+"video"+str(self.id)+".txt", 'w')
            if (os.path.exists(self.video_file)):
                

                fout.write ("Video da convertire: "+filename)
                self.preview_kind=preview_kind
                sourcefile = filename
                try:
                    #anteprima Gia Presente
                    moviemedia=MovieMedia.objects.get(movie=self,file_type=preview_kind,tipo='local')
                    
                except:
                    moviemedia=MovieMedia()
                    moviemedia.movie=self
                    moviemedia.file_type=preview_kind
                    moviemedia.tipo='local'
                    path=settings.PREVIEW_ROOT+str(self.id)+'/'
                    #print path
                    if not os.path.isdir(path):
                        os.mkdir(path)
                    moviemedia.file=settings.PREVIEW_URL+str(self.id)+'/'+str(self.id)+'.'+self.preview_kind
                    #print moviemedia.file
                    flvfilename = "%s.%s" % (self.id , self.preview_kind)
                    targetfile = "%s%s" % (path , flvfilename)
                    try:
                        video_size=settings.VIDEO_SIZE
                    except:
                        video_size='480x360'
                    try:
                        os.remove(targetfile)
                    except:
                        pass
                    sourcefile=sourcefile.replace("'","\\'")
                    
                    if preview_kind=='flv':
                        ffmpeg = "ffmpeg -i '%s' -ss 60 -t 60 -ar 22050 -ab 32 -f flv %s" %(sourcefile, targetfile)
                        flvtool = "flvtool2 -U -duration:6 %s" % targetfile
                        
                    if preview_kind=='ogg':
                        ffmpeg = "ffmpeg -i '%s' -ss 60 -t 60 -acodec libvorbis -ac 1 -b 768k  %s" %(sourcefile,  targetfile)
                        
                    if preview_kind=='mp4':
                        ffmpeg = "ffmpeg -i '%s' -ss 60 -t 60 -f mp4 -vcodec mpeg4 -b 1000k -r 25 -strict experimental -acodec aac -ar 22050 -ab 64k  '%s'" %(sourcefile,  targetfile)
                    
                    #print ffmpeg
                    try:
                        file_ok=True
                        try:
                            fout.write ("1 -------------------- FFMPEG ------------------")
                            #print ffmpeg
                            fout.write(ffmpeg)
                            ffmpegresult = commands.getoutput(ffmpeg)
                            
                            #fout.write (str(ffmpegresult))
                            
                        except:
                            fout.write (" Problemi nella creazione dell'anteprima")
                            
                            # Check if file exists and is > 0 Bytes
                    
                        
                        try:
                            s = os.stat(targetfile)
                            fout.write ("2 s" + str(s))
                            fsize = s.st_size
                            if (fsize == 0):
                                fout.write("3 zero byte?")
                                os.remove(targetfile)
                                file_ok=False
                            fout.write ("4 Dimensione: %i" % fsize)
                            
                        except:
                            fout.write ("5 Il File %s sembra non esistere" % targetfile)
                            file_ok=False
                            
                        
                        
        
                        if (file_ok==True and preview_kind=='flv'):
                            flvresult = commands.getoutput(flvtool)
                            fout.write ("6 -------------------- FLVTOOL ------------------")
                            fout.write (str(flvresult))
                            
                        if (file_ok==True):
                            try:
                                moviemedia.save()
                            except:
                                raise
                                fout.write ('Impossibile salvare')
                                fout.write ( "Unexpected error:" + sys.exc_info()[0])

                        else:
                            fout.write ('Problemi nella generazione del file')
                    except:
                        raise
                        
                    
                    fout.close()
            else:
                fout.write('file video non trovato')
                fout.write( self.video_file )
            
        return None
    
    def ricava_parametri_video (self):
        if self.video_file!=None and self.video_file!='':
            ffmpeg = "ffmpeg -i '%s'" %(self.video_file)
            ffmpegresult = commands.getoutput(ffmpeg)
            pos=ffmpegresult.find('Input #0,')
            pos2=ffmpegresult.find('Output #0',pos)
            tmp=ffmpegresult[pos+len('Input #0,'):pos2].strip()
            
            #print tmp
            #durata
            pos=tmp.find('Duration: ')
            pos2=tmp.find(',',pos)
            self.file_durata=tmp[pos+len('Duration: '):pos2].strip()
            #print 'durata : ' + durata
            
            #bitrate
            pos=tmp.find('bitrate: ')
            pos2=tmp.find('s',pos)
            self.file_bitrate=tmp[pos+len('bitrate: '):pos2+1].strip()
            #print 'bitrate : ' + bitrate
            
            #Dettagli video
            pos=tmp.find('Video: ')
            pos2=tmp.find(chr(10),pos)
            self.file_video=tmp[pos+len('Video: '):pos2].strip()
            #print 'video : ' + Video
            
            #Dettagli audio
            pos=tmp.find('Audio: ')
            pos2=tmp.find(chr(10),pos)
            self.file_audio=tmp[pos+len('Audio: '):pos2].strip()
            #print 'Audio : ' + Audio
           
            self.save()
        else:
            print 'nessun video associato'
        
#def make_preview(sender, instance, signal, *args, **kwargs):
#    if (instance.video_file!='' and instance.video_file!=None):
        #import time
        #instance.create_preview()
#        pass
        #time.sleep(0.2)
        #instance.medium()
        #time.sleep(0.2)
        #instance.micro()

#sig = Signal()

#models.signals.post_save.connect(make_preview, sender=Movie)

class MovieFoto(models.Model):
    CELLSERPRO_CHOICES = (
        ('classic', 'classic'),
        ('locandina', 'locandina'),
        ('cover', 'cover'),
    )
    foto = models.ForeignKey(Photo,verbose_name="Photo")
    movie = models.ForeignKey(Movie,verbose_name="Movie")
    ordine =models.IntegerField(verbose_name="ordine",default=100)
    tipo= models.CharField(verbose_name = "Tipo",max_length=15,choices=CELLSERPRO_CHOICES)
    
    class Meta:
        unique_together = ('foto', 'movie')
        
class MovieLink(models.Model):
    movie = models.ForeignKey(Movie,verbose_name="Film")
    link = models.CharField(verbose_name = "Link",max_length=255)
    tipo = models.CharField(verbose_name = "Tipo",max_length=20)
    download =models.IntegerField(verbose_name="download",blank=True,null=True,default=0)
    
    def __unicode__(self):
        return self.tipo + ' ' +self.movie.titolo 
    
class MovieMedia(models.Model):
    movie = models.ForeignKey(Movie,verbose_name="Film")
    tipo = models.CharField(verbose_name = "Tipo",max_length=20)
    file = models.CharField(verbose_name = "File",max_length=255)
    file_url = models.CharField(verbose_name = "File URL",max_length=255,blank=True,null=True)
    file_type = models.CharField(verbose_name = "tipo_file",max_length=3)
    file_durata=models.CharField(verbose_name='file durata', max_length=20,blank=True,null=True)
    file_bitrate=models.CharField(verbose_name='file bitrate', max_length=20,blank=True,null=True)
    file_audio=models.CharField(verbose_name='file dettagli audio', max_length=255,blank=True,null=True)
    file_video=models.CharField(verbose_name='file_dettagli_video', max_length=255,blank=True,null=True)
    file_size=models.IntegerField(verbose_name="dimensione",blank=True,null=True,default=0)
    
#class foto_old(models.Model):
#    film=models.ForeignKey(Movie,verbose_name="Movie")
#    nome_file=models.CharField(verbose_name = "nome_file",max_length=100)
#    descrizione=models.CharField(verbose_name = "descrizione",max_length=100)
#    peso=models.IntegerField(verbose_name="peso",blank=True,null=True)
#    old_id=models.IntegerField(verbose_name="old_id",blank=True,null=True)
#    
#class persone_old(models.Model):
#    film=models.ForeignKey(Movie,verbose_name="professione")
#    text=models.CharField(verbose_name='text',max_length=200)
#    professione=models.CharField(verbose_name='professione',max_length=10)