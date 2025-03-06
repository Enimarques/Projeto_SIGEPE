from django import forms
from .models import Visita, Visitante

class RegisterForm(forms.ModelForm):#cria um formulario de registro
    class Meta:
        model = Visitante
        fields = ['nome_completo', 'nome_social', 'data_nascimento', 'CPF', 'telefone', 'email', 'estado', 'cidade', 'foto'] #campos do formulario
        labels = {
            'nome_completo': 'Nome completo',
            'nome_social': 'Nome social',
            'data_nascimento': 'Data de nascimento',
            'CPF': 'CPF',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'estado': 'Estado',
            'cidade': 'Cidade',
            'foto': 'Foto',
        }   #muda o nome dos campos pra portugues
        '''widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}), #muda o tipo do campo para data
        }'''
        
class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['visitante', 'setor', 'motivo_visita']
        labels = {
            'visitante': 'Visitante',
            'setor': 'Setor',
            'motivo_visita': 'Motivo da visita',
        }
        
class FimVisitaForm(forms.Form):
    visita = forms.ModelChoiceField(queryset=Visita.objects.filter(data_saida__isnull=True), label='Selecionar visita')
    empty_label = 'Selecione uma visita'
    widgets = forms.Select(attrs={'class': 'form-control'}) #adiciona uma classe ao campo de seleção
    
    
    

    