from django import forms
from persone.models import *

class SearchPersonaForm(forms.Form):
    nome=forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'size':'15'}),
                               label=u'Nome',required=False)
    professione=forms.IntegerField(initial=0,widget=forms.Select(choices = [(professione.pk, professione.professione) for professione in Professioni.objects.all().order_by('id','professione')]),required=False)
    