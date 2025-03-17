from django import forms
from .models import Visita, Visitante, Setor
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
            'bairro',
            'foto'
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
            'bairro': forms.Select(attrs={
                'class': 'form-control'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
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
        return cleaned_data

class VisitaForm(forms.ModelForm):
    cpf = forms.CharField(
        max_length=14,
        validators=[VisitanteForm.cpf_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'id': 'cpf-input'
        })
    )
    
    tipo_setor = forms.ChoiceField(
        choices=[('departamento', 'Departamento'), ('gabinete_vereador', 'Gabinete')],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'tipo-setor'
        }),
        initial='departamento',
        required=True
    )
    
    class Meta:
        model = Visita
        fields = ['cpf', 'setor', 'objetivo', 'observacoes']
        widgets = {
            'setor': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'objetivo': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipo = self.data.get('tipo_setor', 'departamento')
        self.fields['setor'].queryset = Setor.objects.filter(
            tipo=tipo
        ).order_by('nome')
        self.fields['objetivo'].initial = 'outros'
        
        # Configurando widgets com classes Bootstrap
        self.fields['setor'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        self.fields['objetivo'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            raise forms.ValidationError('Por favor, informe o CPF do visitante.')
        
        # Verifica se existe um visitante com este CPF
        try:
            visitante = Visitante.objects.get(CPF=cpf)
            self.visitante = visitante
        except Visitante.DoesNotExist:
            raise forms.ValidationError('CPF não encontrado. Por favor, cadastre o visitante primeiro.')
        
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        tipo_setor = cleaned_data.get('tipo_setor')
        setor = cleaned_data.get('setor')
        
        if setor and tipo_setor and setor.tipo != tipo_setor:
            self.add_error('setor', 'O setor selecionado não corresponde ao tipo escolhido.')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.visitante = self.visitante
        if commit:
            instance.save()
        return instance