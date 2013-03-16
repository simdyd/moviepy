from django import forms
from film.models import *

class SearchForm(forms.Form):
    titolo=forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'size':'15'}),
                               label=u'Titolo',required=False)
    attori=forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'size':'15'}),
                               
                               label=u'Attori',required=False)
    regia=forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'size':'15'}),
                               label=u'Regia',required=False)
    
    genere=forms.IntegerField(initial=0,widget=forms.Select(choices = [(genere.pk, genere.nome) for genere in Genere.objects.all().order_by('id','nome')]),required=False)
    supporto=forms.IntegerField(initial=0,widget=forms.Select(choices = [(supporto.pk, supporto.nome) for supporto in Supporti.objects.all().order_by('nome')]),required=False)