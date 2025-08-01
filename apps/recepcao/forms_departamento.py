from django import forms
from .models import Setor, Assessor

class AlterarHorarioSetorForm(forms.ModelForm):
    """
    Formulário para permitir que assessores alterem o horário de funcionamento 
    do departamento ao qual estão vinculados.
    """
    class Meta:
        model = Setor
        fields = ['horario_abertura', 'horario_fechamento']
        widgets = {
            'horario_abertura': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_fechamento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }

    def __init__(self, *args, **kwargs):
        self.assessor = kwargs.pop('assessor', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        horario_abertura = cleaned_data.get('horario_abertura')
        horario_fechamento = cleaned_data.get('horario_fechamento')

        if horario_abertura and horario_fechamento:
            if horario_abertura >= horario_fechamento:
                raise forms.ValidationError(
                    'O horário de abertura deve ser anterior ao horário de fechamento.'
                )

        return cleaned_data

class SetorForm(forms.ModelForm):
    """
    Formulário para criar/editar Setores
    """
    
    class Meta:
        model = Setor
        fields = [
            'tipo',
            'localizacao',
            'foto',
            'nome_responsavel',
            'funcao',
            'horario_entrada',
            'horario_saida',
            'email',
            'horario_abertura',
            'horario_fechamento',
            'nome_vereador',
            'email_vereador',
            'nome_local'
        ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'localizacao': forms.Select(attrs={
                'class': 'form-control'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'nome_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do responsável'
            }),
            'funcao': forms.Select(attrs={
                'class': 'form-control'
            }),
            'horario_entrada': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_saida': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'horario_abertura': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_fechamento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'nome_vereador': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do vereador'
            }),
            'email_vereador': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'nome_local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do local'
            })
        }
        
    def __init__(self, *args, **kwargs):
        hide_responsavel = kwargs.pop('hide_responsavel', False)
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        tipo = None
        # Tenta pegar o tipo do POST, do instance ou do initial
        if 'tipo' in self.data:
            tipo = self.data.get('tipo')
        elif instance and instance.pk:
            tipo = instance.tipo
        elif 'tipo' in self.initial:
            tipo = self.initial['tipo']

        # Esconde campos de acordo com o tipo e remove obrigatoriedade
        if tipo == 'gabinete':
            if 'nome_local' in self.fields:
                self.fields['nome_local'].widget = forms.HiddenInput()
                self.fields['nome_local'].required = False
        elif tipo == 'departamento':
            if 'nome_vereador' in self.fields:
                self.fields['nome_vereador'].widget = forms.HiddenInput()
                self.fields['nome_vereador'].required = False
            if 'email_vereador' in self.fields:
                self.fields['email_vereador'].widget = forms.HiddenInput()
                self.fields['email_vereador'].required = False

        # Se for edição de gabinete pelo assessor, esconde o campo
        if hide_responsavel or (instance and instance.tipo == 'gabinete'):
            self.fields.pop('nome_responsavel', None)

        # Mostra/esconde campos baseado no tipo
        if instance:
            if instance.tipo == 'gabinete':
                if 'nome_vereador' in self.fields:
                    self.fields['nome_vereador'].required = True
                if 'email_vereador' in self.fields:
                    self.fields['email_vereador'].required = True
                if 'nome_local' in self.fields:
                    self.fields['nome_local'].required = False
            elif instance.tipo == 'departamento':
                if 'nome_local' in self.fields:
                    self.fields['nome_local'].required = True
                if 'nome_vereador' in self.fields:
                    self.fields['nome_vereador'].required = False
                if 'email_vereador' in self.fields:
                    self.fields['email_vereador'].required = False
        
        # Adiciona classes do Select2 para os campos de seleção
        if 'tipo' in self.fields:
            self.fields['tipo'].widget.attrs.update({'class': 'form-control select2'})
        if 'localizacao' in self.fields:
            self.fields['localizacao'].widget.attrs.update({'class': 'form-control select2'})
        if 'funcao' in self.fields:
            self.fields['funcao'].widget.attrs.update({'class': 'form-control select2'})
        
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        horario_abertura = cleaned_data.get('horario_abertura')
        horario_fechamento = cleaned_data.get('horario_fechamento')
        horario_entrada = cleaned_data.get('horario_entrada')
        horario_saida = cleaned_data.get('horario_saida')
        
        # Valida campos obrigatórios baseado no tipo
        if tipo == 'gabinete':
            if not cleaned_data.get('nome_vereador') and 'nome_vereador' in self.fields:
                self.add_error('nome_vereador', 'Este campo é obrigatório para gabinetes.')
            if not cleaned_data.get('email_vereador') and 'email_vereador' in self.fields:
                self.add_error('email_vereador', 'Este campo é obrigatório para gabinetes.')
        elif tipo == 'departamento':
            if not cleaned_data.get('nome_local') and 'nome_local' in self.fields:
                self.add_error('nome_local', 'Este campo é obrigatório para departamentos.')
        
        # Valida horário de funcionamento do setor
        if horario_abertura and horario_fechamento:
            if horario_abertura >= horario_fechamento:
                raise forms.ValidationError(
                    'O horário de abertura do setor deve ser anterior ao horário de fechamento.'
                )
        
        # Valida horário do responsável
        if horario_entrada and horario_saida:
            if horario_entrada >= horario_saida:
                raise forms.ValidationError(
                    'O horário de entrada do responsável deve ser anterior ao horário de saída.'
                )
            
            # Verifica se o horário do responsável está dentro do horário do setor
            if horario_abertura and horario_fechamento:
                if horario_entrada < horario_abertura or horario_saida > horario_fechamento:
                    raise forms.ValidationError(
                        'O horário do responsável deve estar dentro do horário de funcionamento do setor.'
                    )
        
        return cleaned_data

    fieldsets = (
        ('Informações do Gabinete', {
            'fields': ('nome_vereador', 'email_vereador', 'localizacao'),
        }),
        ('Horário de Funcionamento', {
            'fields': ('horario_abertura', 'horario_fechamento'),
        }),
        ('Contato do Assessor', {
            'fields': ('email', 'telefone'),
        }),
        ('Horário do Assessor', {
            'fields': ('horario_entrada', 'horario_saida'),
        }),
    )