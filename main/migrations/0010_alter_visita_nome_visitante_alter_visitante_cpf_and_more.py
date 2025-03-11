# Generated by Django 5.1.6 on 2025-03-10 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_setor_options_alter_visita_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='nome_visitante',
            field=models.CharField(max_length=100, verbose_name='Nome do Visitante'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='CPF',
            field=models.CharField(max_length=14, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='nome_completo',
            field=models.CharField(max_length=100, verbose_name='Nome Completo'),
        ),
    ]
