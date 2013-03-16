from django.db import models
from media.models import Photo

# Create your models here.
class Professioni(models.Model):
    professione = models.CharField(verbose_name = "professione",max_length=50)
    short_id = models.CharField(verbose_name = "short_id",max_length=10)
    
    def __unicode__(self):
        return self.professione
    
class Persona(models.Model):
    nome = models.CharField(verbose_name = "nome",max_length=80)
    cognome = models.CharField(verbose_name = "cognome",max_length=80)
    sesso = models.CharField(verbose_name= "sesso",max_length=1, blank=True, null=True)
    biografia = models.TextField(verbose_name = "biografia", blank=True, null=True)
    data_nascita = models.DateField('Data Nascita',blank=True,null=True)
    luogo_nascita = models.CharField(verbose_name="Luogo di Nascita", max_length=100, blank=True, null=True)
    professione =  models.ManyToManyField(Professioni, verbose_name="Professioni")
    foto = models.ManyToManyField(Photo,verbose_name="Photo", blank=True, null=True)
    
    def getMediumUrl(self):
        tmp=self.get_photo()
        try:
            foto=tmp[0]
        except:
            foto=None
        if foto!=None:
            return foto.getMediumUrl()
        else:
            return None
    
    def getLowUrl(self):
        tmp=self.get_photo()
        try:
            foto=tmp[0]
        except:
            foto=None
        if foto!=None:
            return foto.getLowUrl()
        else:
            return None
        
    
    def thumb(self):
        tmp=self.get_photo()
        try:
            foto=tmp[0]
        except:
            foto=None
        if foto!=None:
            return '<a href="%s"><img width="150" src="%s" /></a>' % (foto.getMediumUrl(), foto.getLowUrl())
        else:
            return '<img width="150" src="none.jpg">'
        
    thumb.allow_tags = True

   
        
    def get_photo(self):
        #foto=self.foto.all()
        #print 'ppp' + self.foto[1].name
        return self.foto.all()
    
    def has_photo(self):
        temp=self.foto.all()
        tmp=len(temp)
        #print tmp
        if tmp>0:    
            return 1
        else:
            return 0
    
    def __unicode__(self):
        return self.nome + ' ' + self.cognome
    
class PersonaLink(models.Model):
    persona = models.ForeignKey(Persona,verbose_name="Persona")
    link = models.TextField(verbose_name = "link", blank=True, null=True)
    tipo_link= models.CharField(verbose_name = "tipo_link",blank=True,null=True,max_length=20)
    download =models.IntegerField(verbose_name="download",blank=True,null=True)