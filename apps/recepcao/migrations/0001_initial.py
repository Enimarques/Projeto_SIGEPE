# Generated by Django 5.1.6 on 2025-03-13 18:02

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Local')),
                ('localizacao', models.CharField(choices=[('terreo', 'Térreo'), ('primeiro_piso', '1° Piso'), ('segundo_piso', '2° Piso')], default='terreo', max_length=20, verbose_name='Localização')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Local de Visita',
                'verbose_name_plural': 'Locais de Visita',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('nome_social', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Social')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('CPF', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')], verbose_name='CPF')),
                ('telefone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Telefone deve estar no formato (XX) XXXXX-XXXX', regex='^\\(\\d{2}\\) \\d{5}-\\d{4}$')], verbose_name='Telefone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('bairro', models.CharField(choices=[('cidade_nova', 'Cidade Nova'), ('primavera', 'Primavera'), ('maranhao', 'Maranhão'), ('rio_verde', 'Rio Verde'), ('nova_vida', 'Nova Vida'), ('uniao', 'União'), ('liberdade_1', 'Liberdade I'), ('liberdade_2', 'Liberdade II'), ('da_paz', 'Da Paz'), ('caetanopolis', 'Caetanópolis'), ('guanabara', 'Guanabara'), ('beira_rio_1', 'Beira Rio I'), ('beira_rio_2', 'Beira Rio II'), ('vila_rica', 'Vila Rica'), ('alto_bonito', 'Alto Bonito'), ('bethania', 'Bethânia'), ('casas_populares', 'Casas Populares'), ('nova_carajas', 'Nova Carajás'), ('tropical', 'Tropical'), ('jardim_canada', 'Jardim Canadá'), ('vila_nova', 'Vila Nova'), ('novo_brasil', 'Novo Brasil'), ('dos_mineiros', 'Dos Mineiros'), ('jardim_america', 'Jardim América'), ('nova_esperanca', 'Nova Esperança'), ('parque_dos_carajas', 'Parque dos Carajás'), ('vale_dos_carajas', 'Vale dos Carajás'), ('novo_horizonte', 'Novo Horizonte'), ('altamira', 'Altamira'), ('vila_sao_jose', 'Vila São José'), ('alto_boa_vista', 'Alto da Boa Vista'), ('outros', 'Outros')], default='outros', max_length=50, verbose_name='Bairro')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='visitantes/', verbose_name='Foto')),
            ],
            options={
                'verbose_name': 'Visitante',
                'verbose_name_plural': 'Visitantes',
                'ordering': ['nome_completo'],
            },
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(choices=[('gabinete_vereador', 'Gabinete de Vereador'), ('departamento', 'Departamento')], default='departamento', max_length=20, verbose_name='Setor')),
                ('localizacao', models.CharField(choices=[('terreo', 'Térreo'), ('plenario', 'Plenário'), ('primeiro_piso', '1° Piso'), ('segundo_piso', '2° Piso')], default='terreo', max_length=20, verbose_name='Localização')),
                ('objetivo', models.CharField(choices=[('reuniao', 'Reunião'), ('entrega', 'Entrega'), ('manutencao', 'Manutenção'), ('evento', 'Evento'), ('outros', 'Outros')], default='outros', max_length=20, verbose_name='Objetivo')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('data_entrada', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data/Hora de Entrada')),
                ('data_saida', models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora de Saída')),
                ('status', models.CharField(choices=[('em_andamento', 'Em Andamento'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada')], default='em_andamento', max_length=20, verbose_name='Status')),
                ('visitante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recepcao.visitante', verbose_name='Visitante')),
            ],
            options={
                'verbose_name': 'Visita',
                'verbose_name_plural': 'Visitas',
                'ordering': ['-data_entrada'],
            },
        ),
    ]
