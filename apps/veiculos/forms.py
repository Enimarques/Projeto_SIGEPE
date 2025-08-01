from django import forms
from .models import Veiculo, HistoricoVeiculo
from django.utils.timezone import make_naive

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'tipo', 'nome_condutor', 'nome_passageiro', 'observacoes']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a placa do veículo'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o modelo do veículo'
            }),
            'cor': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione a cor'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione o tipo'
            }),
            'nome_condutor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do condutor'
            }),
            'nome_passageiro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do passageiro'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite observações relevantes',
                'rows': 3
            })
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            placa = placa.upper().strip()
            # Remove qualquer caractere que não seja letra ou número
            placa = ''.join(c for c in placa if c.isalnum())
            
            # Verifica se a placa já existe
            if Veiculo.objects.filter(placa=placa, data_saida__isnull=True).exists():
                raise forms.ValidationError("Este veículo já está registrado no estacionamento.")
                
            # Valida o formato da placa
            if not Veiculo.validar_placa(placa):
                raise forms.ValidationError("Formato de placa inválido! Use o padrão antigo (ABC1234) ou Mercosul (ABC1D23).")
                
            return placa

class SaidaVeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['veiculo', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Observações sobre a saída'
            })
        }

    veiculo = forms.ModelChoiceField(
        queryset=Veiculo.objects.filter(data_saida__isnull=True),
        empty_label="Selecione o veículo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        veiculo = cleaned_data.get('veiculo')
        data_saida = cleaned_data.get('data_saida')
        if veiculo and data_saida:
            entrada = veiculo.data_entrada
            saida = data_saida
            try:
                entrada = make_naive(entrada)
            except Exception:
                pass
            try:
                saida = make_naive(saida)
            except Exception:
                pass
            diferenca = saida - entrada
            if diferenca.total_seconds() < 60:
                self.add_error('data_saida', 'A saída deve ser pelo menos 1 minuto após a entrada do veículo selecionado.')
        return cleaned_data