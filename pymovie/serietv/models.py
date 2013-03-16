from django.conf import settings
from django.db import models
from persone.models import Persona
from media.models import Photo

from datetime import datetime






class Serietv(models.Model):
    nome = models.CharField(verbose_name = "nome",max_length=50)
    titolo = models.CharField(verbose_name = "titolo",max_length=100,blank=True,null=True)
    titolo_originale = models.CharField(verbose_name = "titolo originale",max_length=100,blank=True,null=True)
    link = models.CharField(verbose_name = "link",max_length=150)
    paese = models.CharField(verbose_name = "paese",max_length=50,blank=True,null=True)
    produzione = models.CharField(verbose_name = "produzione",max_length=50,blank=True,null=True)
    genere = models.CharField(verbose_name = "genere",max_length=50,blank=True,null=True)
    durata = models.CharField(verbose_name = "durata",max_length=50,blank=True,null=True)
    trama = models.TextField(verbose_name = "Trama",blank=True,null=True)

    def __unicode__(self):
        return self.nome

class Episodi(models.Model):
    titolo = models.CharField(verbose_name = "titolo",max_length=100)
    link = models.CharField(verbose_name = "link",max_length=250,blank=True,null=True)
    serietv = models.ForeignKey(Serietv,verbose_name="Serie Tv",blank=True,null=True)
    trama = models.TextField(verbose_name = "Trama",blank=True,null=True)
    stagione = models.IntegerField(verbose_name="stagione",blank=True,null=True)
    episodio = models.IntegerField(verbose_name="episodio",blank=True,null=True)
    data = models.CharField(verbose_name = "data",max_length=15)
    foto = models.ManyToManyField(Photo,verbose_name="Photo", blank=True, null=True)
    visto = models.IntegerField(verbose_name="visto",blank=True,null=True)

    def __unicode__(self):
        return self.titolo

    def thumb(self):
        tmp=self.get_photo()
        try:
            foto=tmp[0]
        except:
            foto=None
        if foto!=None:
            return '<a href="%s"><img width="150" src="%s" />' % (foto.getMediumUrl(), foto.getLowUrl())
        else:
            return '<img width="150" src="none.jpg">'

    thumb.allow_tags = True



    def get_photo(self):
        #foto=self.foto.all()
        #print 'ppp' + self.foto[1].name
        return self.foto.all()

class Supporti(models.Model):
    nome = models.CharField(verbose_name = "nome",max_length=50)
    box = models.CharField(verbose_name = "box",max_length=150)
    posizione = models.IntegerField(verbose_name="Posizione",blank=True,null=True)
    episodi = models.ManyToManyField(Episodi,verbose_name="Episodi", blank=True, null=True)
    serietv = models.ForeignKey(Serietv,verbose_name="Serie Tv",blank=True,null=True)
    stagione = models.IntegerField(verbose_name="stagione",blank=True,null=True)
    episodi_raw= models.CharField(verbose_name = "Episodi Raw",max_length=50,blank=True,null=True)

    def __unicode__(self):
        return self.nome

    def has_episodi(self):
        temp=self.episodi.all()
        tmp=len(temp)
        #print tmp
        if tmp>0:
            return 1
        else:
            return 0

    def link_episodi(self):
        tmp=self.episodi_raw.split(',')

        lista_ep=[]
        print self.episodi.all()
        for ep in tmp:
            tmp2=ep.split('-')
            if len(tmp2)==1:
                tmp3=ep.split('x')
                stagione=self.stagione
                if len(tmp3)==2:
                    stagione=tmp3[0]
                    ep=tmp3[1]


                try:
                    lista_ep.append(int(ep))
                    episodio=Episodi.objects.get(episodio=ep,stagione=stagione,serietv=self.serietv)
                    self.episodi.add(episodio)
                    self.save()
                except:
                    pass
            else:
                tmp3=tmp2[0].split('x')
                stagione=self.stagione
                if len(tmp3)==2:
                    stagione=tmp3[0]
                    aa=int(tmp3[1])
                else:
                    aa=int(tmp2[0])
                while aa<=int(tmp2[1]):
                    try:

                        lista_ep.append(int(aa))
                        episodio=Episodi.objects.get(episodio=aa,stagione=stagione,serietv=self.serietv)
                        self.episodi.add(episodio)
                        self.save()
                    except:
                        pass
                    aa+=1
        print self.episodi.all()
        #print self.episodi.all
        #self.episodi_raw=''
        #self.save()

    class Meta:
        ordering = ['box','posizione',]





