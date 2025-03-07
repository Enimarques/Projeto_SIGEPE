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
    cpf = forms.CharField(max_length=14, label='CPF') #cria um campo de cpf
    nome_visitante = forms.CharField(label='Nome do Visitante', max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))    
    
    class Meta:
        model = Visita
        fields = ['cpf', 'nome_visitante','setor', 'motivo_visita']
        labels = {
            'cpf': 'CPF do Visitante',
            'nome_visitante': 'Nome do Visitante',
            'setor': 'Setor',
            'motivo_visita': 'Motivo da visita',
        }
        
class FimVisitaForm(forms.Form):
    visita = forms.ModelChoiceField(queryset=Visita.objects.filter(data_saida__isnull=True), label='Selecionar visita')
    empty_label = 'Selecione uma visita'
    widgets = forms.Select(attrs={'class': 'form-control'}) #adiciona uma classe ao campo de seleção
    
    
    

    