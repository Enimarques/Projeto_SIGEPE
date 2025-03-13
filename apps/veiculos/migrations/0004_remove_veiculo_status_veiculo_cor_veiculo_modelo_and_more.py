# Generated by Django 5.1.6 on 2025-03-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0003_delete_movimentaçãoveiculo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='veiculo',
            name='status',
        ),
        migrations.AddField(
            model_name='veiculo',
            name='cor',
            field=models.CharField(default='Não informada', max_length=20),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='modelo',
            field=models.CharField(default='Não informado', max_length=50),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='tipo',
            field=models.CharField(choices=[('Carro', 'Carro'), ('Moto', 'Moto'), ('Caminhonete', 'Caminhonete')], default='Carro', max_length=15),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='placa',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]
