from django import forms
from .models import Veiculo

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'tipo', 'responsavel', 'observacoes', 'status']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234 ou ABC1D23'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Gol, Civic, etc.'
            }),
            'cor': forms.RadioSelect(attrs={'class': 'color-grid'}),
            'tipo': forms.RadioSelect(attrs={'class': 'tipo-grid'}),
            'responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do responsável'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Observações adicionais'
            }),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_placa(self):
        """ Validação da placa dentro do formulário """
        placa = self.cleaned_data['placa'].upper()
        if not Veiculo.validar_placa(placa):
            raise forms.ValidationError("Formato de placa inválido! Use o padrão antigo (ABC-1234) ou Mercosul (ABC1D23).")
        return placa

class SaidaVeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'horario_saida', 'observacoes', 'status']
        
        widgets = {
            'horario_saida': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Observações sobre a saída'
            }),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    # Puxa os veículos já cadastrados, para facilitar a seleção
    placa = forms.ModelChoiceField(
        queryset=Veiculo.objects.filter(horario_saida__isnull=True),
        empty_label="Selecione o veículo",
        to_field_name="placa",
        widget=forms.Select(attrs={'class': 'form-control'})
    )