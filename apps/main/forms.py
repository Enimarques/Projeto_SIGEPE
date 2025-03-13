from django import forms
from .models import Visita, Visitante
from django.core.validators import RegexValidator

class VisitanteForm(forms.ModelForm):
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='Digite um CPF válido no formato XXX.XXX.XXX-XX'
    )
    
    telefone_validator = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message='Digite um telefone válido no formato (XX) XXXXX-XXXX'
    )

    CPF = forms.CharField(
        max_length=14,
        validators=[cpf_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00'
        })
    )

    telefone = forms.CharField(
        max_length=15,
        validators=[telefone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000'
        })
    )

    class Meta:
        model = Visitante
        fields = [
            'nome_completo', 
            'nome_social', 
            'data_nascimento', 
            'CPF', 
            'telefone', 
            'email', 
            'estado', 
            'cidade', 
            'foto',
            'objetivo_visita',
            'descricao_outros'
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do visitante'
            }),
            'nome_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome social (se houver)'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'objetivo_visita': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descricao_outros': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva o objetivo da visita'
            })
        }

    def clean_nome_completo(self):
        nome_completo = self.cleaned_data.get('nome_completo')
        if not nome_completo:
            raise forms.ValidationError('O nome completo é obrigatório.')
        return nome_completo

    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        if not cpf:
            raise forms.ValidationError('O CPF é obrigatório.')
        # Verifica se já existe um visitante com este CPF
        if Visitante.objects.filter(CPF=cpf).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        objetivo_visita = cleaned_data.get('objetivo_visita')
        descricao_outros = cleaned_data.get('descricao_outros')
        
        if objetivo_visita == 'outros' and not descricao_outros:
            raise forms.ValidationError({
                'descricao_outros': 'Por favor, forneça uma descrição quando selecionar "Outros".'
            })
        
        return cleaned_data

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['visitante', 'observacoes']
        widgets = {
            'visitante': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais'
            })
        }

    def clean_visitante(self):
        visitante = self.cleaned_data.get('visitante')
        if not visitante:
            raise forms.ValidationError('Por favor, selecione um visitante.')
        return visitante