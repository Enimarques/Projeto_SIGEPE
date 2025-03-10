# Generated by Django 5.1.6 on 2025-03-03 15:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimentaçãoveiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('horario_saida', models.DateTimeField(blank=True, null=True)),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veiculos.veiculo')),
            ],
        ),
    ]
