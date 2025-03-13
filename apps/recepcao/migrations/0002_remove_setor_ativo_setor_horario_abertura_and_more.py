# Generated by Django 5.1.6 on 2025-03-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepcao', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setor',
            name='ativo',
        ),
        migrations.AddField(
            model_name='setor',
            name='horario_abertura',
            field=models.TimeField(blank=True, null=True, verbose_name='Horário de Abertura'),
        ),
        migrations.AddField(
            model_name='setor',
            name='horario_fechamento',
            field=models.TimeField(blank=True, null=True, verbose_name='Horário de Fechamento'),
        ),
    ]
