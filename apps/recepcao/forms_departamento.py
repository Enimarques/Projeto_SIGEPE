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
    Formulário para criar/editar Setores com seleção de responsável
    """
    nome_responsavel = forms.ModelChoiceField(
        queryset=Assessor.objects.filter(ativo=True, departamento__isnull=False),
        label='Responsável',
        required=False,
        empty_label="Selecione um responsável",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Selecione um responsável'
        })
    )
    
    class Meta:
        model = Setor
        fields = [
            'tipo',
            'localizacao',
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
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        # Se for edição, filtra os assessores pelo tipo do setor
        if instance:
            self.fields['nome_responsavel'].queryset = Assessor.objects.filter(
                ativo=True,
                departamento__isnull=False
            ).order_by('nome_responsavel')
            
            # Se já existe um responsável, pré-seleciona ele
            if instance.nome_responsavel:
                try:
                    assessor = Assessor.objects.get(
                        nome_responsavel=instance.nome_responsavel,
                        ativo=True
                    )
                    self.fields['nome_responsavel'].initial = assessor.id
                except Assessor.DoesNotExist:
                    pass
            
            # Mostra/esconde campos baseado no tipo
            if instance.tipo == 'gabinete':
                self.fields['nome_vereador'].required = True
                self.fields['email_vereador'].required = True
                self.fields['nome_local'].required = False
            elif instance.tipo == 'departamento':
                self.fields['nome_local'].required = True
                self.fields['nome_vereador'].required = False
                self.fields['email_vereador'].required = False
        
        # Adiciona classes do Select2 para os campos de seleção
        self.fields['tipo'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['localizacao'].widget.attrs.update({'class': 'form-control select2'})
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
            if not cleaned_data.get('nome_vereador'):
                self.add_error('nome_vereador', 'Este campo é obrigatório para gabinetes.')
            if not cleaned_data.get('email_vereador'):
                self.add_error('email_vereador', 'Este campo é obrigatório para gabinetes.')
        elif tipo == 'departamento':
            if not cleaned_data.get('nome_local'):
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
        
    def save(self, commit=True):
        setor = super().save(commit=False)
        assessor = self.cleaned_data.get('nome_responsavel')
        
        if assessor:
            setor.nome_responsavel = assessor.nome_responsavel
            setor.email = assessor.email
            setor.funcao = assessor.funcao
            setor.horario_entrada = assessor.horario_entrada
            setor.horario_saida = assessor.horario_saida
            
        if commit:
            setor.save()
            
        return setor