from django import forms
from .models import Setor

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