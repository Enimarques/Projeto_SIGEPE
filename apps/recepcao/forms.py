from django import forms
from .models import Visita, Visitante, Setor
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

class VisitanteForm(forms.ModelForm):
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='Digite um CPF válido no formato XXX.XXX.XXX-XX'
    )
    
    telefone_validator = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message='Digite um telefone válido no formato (XX) XXXXX-XXXX'
    )

    cep_validator = RegexValidator(
        regex=r'^\d{5}-\d{3}$',
        message='Digite um CEP válido no formato 00000-000'
    )

    data_validator = RegexValidator(
        regex=r'^\d{2}/\d{2}/\d{4}$',
        message='Digite uma data válida no formato dd/mm/aaaa'
    )

    CPF = forms.CharField(
        max_length=14,   
        validators=[cpf_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'data-mask': 'cpf',
            'required': True
        })
    )

    telefone = forms.CharField(
        max_length=15,
        validators=[telefone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000',
            'data-mask': 'telefone',
            'required': True
        })
    )

    data_nascimento = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa',
            'data-mask': 'data',
            'required': True
        })
    )

    CEP = forms.CharField(
        max_length=9,
        validators=[cep_validator],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000',
            'data-mask': 'cep'
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
            'logradouro',
            'numero',
            'complemento',
            'CEP',
            'foto'
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do visitante',
                'required': True
            }),
            'nome_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome social (se houver)'
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
            'logradouro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, etc. (Opcional)'
            })
        }

    def clean_nome_completo(self):
        nome_completo = self.cleaned_data.get('nome_completo')
        if not nome_completo:
            raise forms.ValidationError('O nome completo é obrigatório.')
        return nome_completo

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if not data_nascimento:
            raise forms.ValidationError('A data de nascimento é obrigatória.')
        
        # Verificar idade mínima de 18 anos
        idade_minima = timezone.now().date() - timedelta(days=18*365)
        if data_nascimento > idade_minima:
            raise forms.ValidationError('Você deve ter pelo menos 18 anos.')
        
        return data_nascimento

    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        if not cpf:
            raise forms.ValidationError('O CPF é obrigatório.')
        
        # Remover pontos e traço para validação
        cpf_numerico = cpf.replace('.', '').replace('-', '')
        
        # Validação de CPF
        if len(cpf_numerico) != 11:
            raise forms.ValidationError('CPF inválido.')
        
        # Verificar se todos os dígitos são iguais
        if len(set(cpf_numerico)) == 1:
            raise forms.ValidationError('CPF inválido.')
        
        # Cálculo dos dígitos verificadores
        def calcula_digito_verificador(cpf_parcial):
            soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i) for i in range(len(cpf_parcial)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Verificar primeiro dígito verificador
        digito1 = calcula_digito_verificador(cpf_numerico[:9])
        if int(cpf_numerico[9]) != digito1:
            raise forms.ValidationError('CPF inválido.')
        
        # Verificar segundo dígito verificador
        digito2 = calcula_digito_verificador(cpf_numerico[:10])
        if int(cpf_numerico[10]) != digito2:
            raise forms.ValidationError('CPF inválido.')
        
        # Verificar se já existe um visitante com este CPF
        if Visitante.objects.filter(CPF=cpf).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone:
            raise forms.ValidationError('O telefone é obrigatório.')
        
        # Remover caracteres não numéricos
        telefone_numerico = ''.join(filter(str.isdigit, telefone))
        
        # Verificar se tem 10 ou 11 dígitos
        if len(telefone_numerico) < 10 or len(telefone_numerico) > 11:
            raise forms.ValidationError('Número de telefone inválido.')
        
        # Verificar se os primeiros dígitos são válidos
        ddd = telefone_numerico[:2]
        
        # Lista de DDDs válidos
        ddds_validos = [
            '11', '12', '13', '14', '15', '16', '17', '18', '19',  # São Paulo
            '21', '22', '24', '27', '28',  # Rio de Janeiro
            '31', '32', '33', '34', '35', '37', '38',  # Minas Gerais
            '41', '42', '43', '44', '45', '46',  # Paraná
            '47', '48', '49',  # Santa Catarina
            '51', '53', '54', '55',  # Rio Grande do Sul
            '61',  # Distrito Federal
            '62', '64',  # Goiás
            '63',  # Tocantins
            '65', '66',  # Mato Grosso
            '67',  # Mato Grosso do Sul
            '68',  # Acre
            '69',  # Rondônia
            '71', '73', '74', '75', '77',  # Bahia
            '79',  # Sergipe
            '81', '87',  # Pernambuco
            '82',  # Alagoas
            '83',  # Paraíba
            '84',  # Rio Grande do Norte
            '85', '88',  # Ceará
            '86', '89',  # Piauí
            '91', '93', '94',  # Pará
            '92', '97',  # Amazonas
            '95',  # Roraima
            '96',  # Amapá
        ]
        
        if ddd not in ddds_validos:
            raise forms.ValidationError('DDD inválido.')
        
        return telefone

    def clean_CEP(self):
        cep = self.cleaned_data.get('CEP')
        if cep:
            # Remover caracteres não numéricos
            cep_numerico = ''.join(filter(str.isdigit, cep))
            if len(cep_numerico) != 8:
                raise forms.ValidationError('CEP inválido.')
        return cep

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se estiver editando, tornar o CPF somente leitura
        if self.instance and self.instance.pk:
            self.fields['CPF'].widget.attrs['readonly'] = True

class VisitaForm(forms.ModelForm):
    cpf = forms.CharField(
        max_length=14,
        validators=[VisitanteForm.cpf_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'data-mask': 'cpf',
            'id': 'cpf-input'
        })
    )
    
    tipo_setor = forms.ChoiceField(
        choices=Setor.TIPO_CHOICES,
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
        
        # Carregar todos os setores para permitir filtragem via JavaScript
        setores = Setor.objects.all().order_by('tipo', 'nome_vereador', 'nome_local')
        self.fields['setor'].queryset = setores
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