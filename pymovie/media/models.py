from django.db import models
from django.db.models import signals
import os, Image
from django.conf import settings

from datetime import datetime

# Create your models here.
try :
    MICRO_SIZE = settings.MICRO_SIZE
    TINY_SIZE = settings.TINY_SIZE
    MEDIUM_SIZE = settings.MEDIUM_SIZE
except:
    MICRO_SIZE = (50,50)
    TINY_SIZE = (170,170)    #thumb size (x,y)
    #MEDIUM_SIZE = (253,253)    #thumb size (x,y)
    MEDIUM_SIZE = (600,600)    #thumb size (x,y)

try:
    FILE_SEPARATOR = settings.FILE_SEPARATOR
except:
    FILE_SEPARATOR = os.sep
    
class Photo(models.Model):
    name = models.CharField(verbose_name='Nome',max_length=50 ,blank=False)
    image = models.ImageField(verbose_name='Immagine', upload_to="%Y/%m/")
    caption = models.TextField(verbose_name='Didascalia', max_length=4000, blank=False)
    photographer = models.CharField(verbose_name='Fotografo', max_length=50 ,blank=True)
    upload_date = models.DateTimeField('data upload',blank=True,null=True,default=datetime.now)
    publish_date = models.DateTimeField('data pubblicazione',blank=True,null=True,default=datetime.now)
    expiry_date = models.DateTimeField('data scadenza',blank=True,null=True,default=datetime.now)
    
    def upload(self, url):
        image_url = urllib2.urlopen(url)
        image = Image.open(StringIO.StringIO(image_url.read()), 'r')
        name = settings.MEDIA_ROOT + datetime.now().strftime("/%Y/%m/") + self.name
        self.image = name
        image = image.save(name)
        os.chmod(name, 0777)

    def low(self,force=False):
        if (self.image.name.find(settings.MEDIA_ROOT) >= 0):
            image_path = self.image.name[len(settings.MEDIA_ROOT):]
        else:
            image_path = self.image.name

        tinythumb = (settings.MEDIA_ROOT +  image_path).split(FILE_SEPARATOR)
        tinythumb = FILE_SEPARATOR.join(tinythumb)

        ext = tinythumb[tinythumb.rindex('.'):]
        ext_ = ext.lower()
        if ext_=='.jpeg' or ext_=='.jpg':
            tinythumb = tinythumb.replace(ext,'_low.jpg')
        if ext_=='.gif':
            tinythumb = tinythumb.replace(ext,'_low.gif')
            
        if (not os.path.exists(tinythumb) or force == True):
            im = Image.open(settings.MEDIA_ROOT + image_path, 'r')
            size=TINY_SIZE
            rx, ry = im.size[0]/float(size[0]), im.size[1]/float(size[1])
            
            resize = int(size[0]), int(round(im.size[1]*(1.0/rx), 0))
            
            try:    
                im.thumbnail(resize,Image.ANTIALIAS)
            except:
                im.thumbnail(TINY_SIZE,Image.ANTIALIAS)
            if ext_=='.jpeg' or ext_=='.jpg':
                im.save(tinythumb,"JPEG", dpi=(72, 72), quality=80)
            if ext_=='.gif':
                im.save(tinythumb,"GIF", dpi=(72, 72), quality=80)
            os.chmod(tinythumb, 0777)
        p = tinythumb.split(FILE_SEPARATOR)
        low_name = p[-1]

        low_path = image_path

        p2 = low_path.split(FILE_SEPARATOR)
        temp = p2[:-1]
        low_path = temp[0]+FILE_SEPARATOR+temp[1]+FILE_SEPARATOR+ low_name
        low_path = low_path.replace(FILE_SEPARATOR,'/')
        return '<a href="%s"><img src="%s" alt="tiny thumbnail image" />' % (settings.MEDIA_URL +image_path,settings.MEDIA_URL+low_path)



    def medium(self,force=False):
        if (self.image.name.find(settings.MEDIA_ROOT) >= 0):
            image_path = self.image.name[len(settings.MEDIA_ROOT):]
        else:
            image_path = self.image.name

        mediumsize = (settings.MEDIA_ROOT +  image_path).split(FILE_SEPARATOR)
        mediumsize = '/'.join(mediumsize)

        ext = mediumsize[mediumsize.rindex('.'):]
        ext_ = ext.lower()
        if ext_=='.jpeg' or ext_=='.jpg':
            mediumsize = mediumsize.replace(ext,'_medium.jpg')
        if ext_=='.gif':
            mediumsize = mediumsize.replace(ext,'_medium.gif')
        

        if (not os.path.exists(mediumsize)  or force == True):
            im = Image.open(settings.MEDIA_ROOT +  image_path, 'r')
            
            size=MEDIUM_SIZE
            rx, ry = im.size[0]/float(size[0]), im.size[1]/float(size[1])
            
            resize = int(size[0]), int(round(im.size[1]*(1.0/rx), 0))
            
            try:
                im.thumbnail(resize,Image.ANTIALIAS)
            except:
                im.thumbnail(MEDIUM_SIZE,Image.ANTIALIAS)
            if ext_=='.jpeg' or ext_=='.jpg':
                im.save(mediumsize,"JPEG", dpi=(72, 72), quality=80)
            if ext_=='.gif':
                im.save(mediumsize,"GIF", dpi=(72, 72), quality=80)
            os.chmod(mediumsize, 0777)
        return '<a href="%s"><img src="%s" alt="medium image" />' % (settings.MEDIA_URL +image_path,settings.MEDIA_URL+mediumsize)

    def micro(self):
        if (self.image.name.find(settings.MEDIA_ROOT) >= 0):
            image_path = self.image.name[len(settings.MEDIA_ROOT):]
        else:
            image_path = self.image.name

        microsize = (settings.MEDIA_ROOT +  image_path).split(FILE_SEPARATOR)
        microsize = '/'.join(microsize)

        ext = microsize[microsize.rindex('.'):]
        ext_ = ext.lower()
        if ext_=='.jpeg' or ext_=='.jpg':
            microsize = microsize.replace(ext,'_micro.jpg')
        if ext_=='.gif':
            microsize = microsize.replace(ext,'_micro.gif')

        if not os.path.exists(microsize):
            im = Image.open(settings.MEDIA_ROOT +  image_path, 'r')
            size=MICRO_SIZE
            rx, ry = im.size[0]/float(size[0]), im.size[1]/float(size[1])
            
            resize = int(size[0]), int(round(im.size[1]*(1.0/rx), 0))
            
            try:    
                im.thumbnail(resize,Image.ANTIALIAS)
            except:
                im.thumbnail(MICRO_SIZE,Image.ANTIALIAS)
            if ext_=='.jpeg' or ext_=='.jpg':
                im.save(microsize,"JPEG", dpi=(72, 72), quality=30)
            if ext_=='.gif':
                im.save(microsize,"GIF", dpi=(72, 72), quality=30)
            os.chmod(microsize, 0777)
        return '<a href="%s"><img src="%s" alt="micro image" /></a>' % (settings.MEDIA_URL +image_path,settings.MEDIA_URL+microsize)

    class Meta:
        verbose_name = 'Immagine'
        verbose_name_plural = 'Immagini'
    
    def getUrl(self):
        image_path = self.image.name
        toRet = settings.MEDIA_URL
        if toRet.endswith('/') or toRet.endswith('\\'):
            toRet = toRet + image_path
        else:
            toRet = toRet + "/" +image_path
        return toRet.replace('\\','/')

    def getLowUrl(self):
            image_path = self.image.name
            #print image_path
            p = image_path
            #print '22222' + p
            if p is None or p == '':
                return ''
            try:
                ext = p[p.rindex('.'):]
            except:
                return None
            ext_ = ext.lower()
            if ext_=='.jpeg' or ext_=='.jpg':
                p = p.replace(ext,'_low.jpg')
            if ext_=='.gif':
                p = p.replace(ext,'_low.gif')
            
            
            p = p.split(FILE_SEPARATOR)
            low_name = p[-1]
            low_path = image_path
            p2 = low_path.split(FILE_SEPARATOR)
            temp = p2[:-1]
            low_path = temp[0]+"/"+temp[1]+"/"+ low_name
            #print low_path
            return settings.MEDIA_URL+low_path
        

    def getSite(self):
        return self.id_site.all()[0].name

    def getMediumUrl(self):
        try :
            if (self.image.name.find(settings.MEDIA_ROOT) >= 0):
                image_path = self.image.name[len(settings.MEDIA_ROOT):]
            else:
                image_path = self.image.name

            p = image_path
            if p is None or p == '':
                return ''

            ext = p[p.rindex('.'):]
            ext_ = ext.lower()
            if ext_=='.jpeg' or ext_=='.jpg':
                p = p.replace(ext,'_medium.jpg')
            if ext_=='.gif':
                p = p.replace(ext,'_medium.gif')
            if not os.path.exists(settings.MEDIA_ROOT + p):
                p = image_path

            return settings.MEDIA_URL+p
        except :
            return ''

    def getMicroUrl(self):
        try :
            if (self.image.name.find(settings.MEDIA_ROOT) >= 0):
                image_path = self.image.name[len(settings.MEDIA_ROOT):]
            else:
                image_path = self.image.name

            p = image_path
            if p is None or p == '':
                return ''

            ext = p[p.rindex('.'):]
            ext_ = ext.lower()
            if ext_=='.jpeg' or ext_=='.jpg':
                p = p.replace(ext,'_micro.jpg')
            if ext_=='.gif':
                p = p.replace(ext,'_micro.gif')
            if not os.path.exists(settings.MEDIA_ROOT + p):
                p = image_path

            return settings.MEDIA_URL+p
        except :
            return ''

    def thumb(self):
        return '<a href="%s"><img width="150" src="%s" alt="tiny thumbnail image" /></a>' % (self.getMediumUrl(), self.getLowUrl())

    thumb.allow_tags = True

    def get_image_url (self) :
        if (self.image.name.find(settings.MEDIA_ROOT) >= 0 ):
            path =  self.image.name[len(settings.MEDIA_ROOT):]
        else:
            path =  self.image.name

        return settings.MEDIA_URL+path

    def __unicode__(self):
        return self.name
    
def make_res(sender, instance, signal, *args, **kwargs):
    if (instance.image):
        import time
        instance.low()
        time.sleep(0.2)
        instance.medium()
        time.sleep(0.2)
        instance.micro()

#sig = Signal()

models.signals.post_save.connect(make_res, sender=Photo)

class Gallery(models.Model):
    id_object = models.ManyToManyField(Photo,verbose_name='Immagine', related_name = 'immagini')
    title = models.CharField(verbose_name='Titolo',max_length=100)
    description = models.TextField(verbose_name='Descrizione',max_length=1000,blank=True,null=True)
    publish_date = models.DateTimeField('data pubblicazione',blank=True,null=True)
    expiry_date = models.DateTimeField('data scadenza',blank=True,null=True)
    is_published = models.BooleanField(verbose_name='Pubblicato',default=False)

    def get_photos (self):
        #return self.id_object.all()
        #order_by('-m2m_media_objects_photo__immagini.id');
        return self.id_object.order_by('-media_objects_gallery_id_object.id')

    def Sezione (self):
        try:
            toret = ''
            for s in self.id_section.all():
                toret=toret+", "+s.section_name
            if len(toret)>0:
                toret = toret[1:]
        except:
            toret = ''
        return toret


    class Meta:
        verbose_name = 'Galleria'
        verbose_name_plural = 'Gallerie'

    def __unicode__(self):
        return self.title

    