from django.db import migrations
from django.utils import timezone

def popular_historico(apps, schema_editor):
    Veiculo = apps.get_model('veiculos', 'Veiculo')
    HistoricoVeiculo = apps.get_model('veiculos', 'HistoricoVeiculo')
    
    # Para cada veículo existente
    for veiculo in Veiculo.objects.all():
        # Criar registro de entrada
        HistoricoVeiculo.objects.create(
            veiculo=veiculo,
            data_entrada=veiculo.data_entrada,
            data_saida=veiculo.data_saida,
            visitante=veiculo.visitante
        )

class Migration(migrations.Migration):
    dependencies = [
        ('veiculos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(popular_historico),
    ] 