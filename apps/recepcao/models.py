from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from datetime import datetime, time

class Setor(models.Model):
    TIPO_CHOICES = [
        ('gabinete_vereador', 'Gabinete'),
        ('departamento', 'Departamento')
    ]
    
    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('primeiro_piso', '1° Piso'),
        ('segundo_piso', '2° Piso'),
    ]
    
    FUNCAO_CHOICES = [
        ('assessor_1', 'Assessor I'),
        ('assessor_2', 'Assessor II'),
        ('assessor_3', 'Assessor III'),
        ('assessor_4', 'Assessor IV'),
        ('assessor_5', 'Assessor V'),
        ('assessor_6', 'Assessor VI'),
        ('assessor_7', 'Assessor VII'),
        ('assessor_8', 'Assessor VIII'),
        ('assessor_9', 'Assessor IX'),
        ('assessor_10', 'Assessor X'),
        ('agente_parlamentar', 'Agente Parlamentar'),
        ('Chefe_de_Gabinete', 'Chefe de Gabinete'),
        ('Chefe_de_Departamento', 'Chefe de Departamento'),
        ('outros', 'Outros')
    ]

    nome = models.CharField('Nome do Local', max_length=100)
    nome_responsavel = models.CharField('Nome do Responsável', max_length=100, blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='departamento')
    localizacao = models.CharField('Localização', max_length=20, choices=LOCALIZACAO_CHOICES, default='terreo')
    horario_abertura = models.TimeField('Horário de Abertura', blank=True, null=True)
    horario_fechamento = models.TimeField('Horário de Fechamento', blank=True, null=True)
    
    # Campos migrados do modelo Assessor
    nome_responsavel = models.CharField('Nome do Responsável', max_length=100, blank=True, null=True)
    funcao = models.CharField('Função/Cargo', max_length=21, choices=FUNCAO_CHOICES, blank=True, null=True)
    horario_entrada = models.TimeField('Horário de Entrada', blank=True, null=True)
    horario_saida = models.TimeField('Horário de Saída', blank=True, null=True)
    email = models.EmailField('E-mail', max_length=255, blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)
    usuario = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='setor_responsavel', verbose_name='Usuário')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nome']

    def __str__(self):
        tipo_display = 'Gabinete' if self.tipo == 'gabinete_vereador' else 'Departamento'
        return f'{self.nome} ({tipo_display})'

    def esta_aberto(self):
        if not self.horario_abertura or not self.horario_fechamento:
            return None  # Retorna None se não tiver horário definido
            
        agora = timezone.localtime().time()
        return self.horario_abertura <= agora <= self.horario_fechamento

    def status_funcionamento(self):
        esta_aberto = self.esta_aberto()
        if esta_aberto is None:
            return "Horário não definido"
        return "Aberto" if esta_aberto else "Fechado"

    def get_horario_trabalho(self):
        if not self.horario_entrada or not self.horario_saida:
            return 'Horário não definido'
        try:
            if self.horario_entrada is None or self.horario_saida is None:
                return 'Horário não definido'
            return f'{self.horario_entrada.strftime("%H:%M")} - {self.horario_saida.strftime("%H:%M")}'
        except AttributeError:
            return 'Horário não definido'

    def get_status_presenca(self):
        if not self.horario_entrada or not self.horario_saida:
            return 'Horário não definido'
            
        agora = timezone.localtime().time()
        if self.horario_entrada <= agora <= self.horario_saida:
            return 'Presente'
        return 'Ausente'

    def clean(self):
        # Validar se o horário do responsável está dentro do horário do setor
        if self.horario_entrada and self.horario_saida and self.horario_abertura and self.horario_fechamento:
            if self.horario_entrada < self.horario_abertura or self.horario_saida > self.horario_fechamento:
                raise ValidationError('O horário do responsável deve estar dentro do horário de funcionamento do setor.')
        super().clean()

class Assessor(models.Model):
    FUNCAO_CHOICES = [
        ('assessor_1', 'Assessor I'),
        ('assessor_2', 'Assessor II'),
        ('assessor_3', 'Assessor III'),
        ('assessor_4', 'Assessor IV'),
        ('assessor_5', 'Assessor V'),
        ('assessor_6', 'Assessor VI'),
        ('assessor_7', 'Assessor VII'),
        ('assessor_8', 'Assessor VIII'),
        ('assessor_9', 'Assessor IX'),
        ('assessor_10', 'Assessor X'),
        ('agente_parlamentar', 'Agente Parlamentar'),
        ('outros', 'Outros')
    ]

    nome = models.CharField('Nome', max_length=100)
    departamento = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name='Departamento')
    funcao = models.CharField('Função/Cargo', max_length=20, choices=FUNCAO_CHOICES)
    horario_entrada = models.TimeField('Horário de Entrada')
    horario_saida = models.TimeField('Horário de Saída')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)
    email = models.EmailField('E-mail', max_length=255, blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)
    usuario = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assessor', verbose_name='Usuário')

    class Meta:
        verbose_name = 'Assessor'
        verbose_name_plural = 'Assessores'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} - {self.get_funcao_display()} ({self.departamento.nome})'

    def clean(self):
        # Validar se o horário do assessor está dentro do horário do departamento
        if self.departamento and self.departamento.horario_abertura and self.departamento.horario_fechamento:
            if self.horario_entrada < self.departamento.horario_abertura or self.horario_saida > self.departamento.horario_fechamento:
                raise ValidationError('O horário do assessor deve estar dentro do horário de funcionamento do departamento.')


class Visitante(models.Model):
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    BAIRROS_CHOICES = [
        ('alto_boa_vista', 'Alto da Boa Vista'),
        ('alto_bonito', 'Alto Bonito'),
        ('altamira', 'Altamira'),
        ('amazonia', 'Amazônia'),
        ('alvora', 'Alvorá'),
        ('apoena', 'Apoena'),
        ('amec_ville_jacaranda', 'Amec Ville Jacarandá'),
        ('beira_rio_1', 'Beira Rio I'),
        ('beira_rio_2', 'Beira Rio II'),
        ('belvedere', 'Belvedere'),
        ('betania', 'Betânia'),
        ('brasilia', 'Brasília'),
        ('bom_jesus', 'Bom Jesus'),
        ('caetanopolis', 'Caetanópolis'),
        ('casas_populares_1', 'Casas Populares I'),
        ('casas_populares_2', 'Casas Populares II'),
        ('california', 'California'),
        ('cedere_1', 'Cedere I'),
        ('cedere_2', 'Cedere II'),
        ('centro', 'Centro'),
        ('cidade_jardim', 'Cidade Jardim'),
        ('cidade_nova', 'Cidade Nova'),
        ('chacara_belo_vale', 'Chacara Belo Vale'),
        ('chacara_da_lua', 'Chacara da Lua'),
        ('chacara_das_estrelas', 'Chacara das Estrelas'),
        ('chacara_do_sol', 'Chacara do Sol'),
        ('chacara_do_cacau', 'Chacara do Cacau'),
        ('colonia_paulo_fonteles', 'Colônia Paulo Fonteles'),
        ('conjunto_hab_morar_dias_melhores', 'Conjunto Hab Morar Dias Melhores'),
        ('da_paz', 'Da Paz'),
        ('dos_mineiros', 'Dos Mineiros'),
        ('distrito_industrial', 'Distrito Industrial'),
        ('esplanada', 'Esplanada'),
        ('esperanca', 'Esperança'),
        ('fap', 'FAP'),
        ('fazenda_santo_antonio', 'Fazenda Santo Antônio'),
        ('fazenda_sao_jose', 'Fazenda São José'),
        ('fazenda_serra_grande', 'Fazenda Serra Grande'),
        ('guanabara', 'Guanabara'),
        ('habitar_feliz', 'Habitar Feliz'),
        ('ipiranga', 'Ipiranga'),
        ('jardim_america', 'Jardim América'),
        ('jardim_canada', 'Jardim Canadá'),
        ('jardim_planalto', 'Jardim Planalto'),
        ('jardim_ipiranga', 'Jardim Ipiranga'),
        ('jardim_novo_horizonte', 'Jardim Novo Horizonte'),
        ('liberdade_1', 'Liberdade I'),
        ('liberdade_2', 'Liberdade II'),
        ('linha_verde', 'Linha Verde'),
        ('loteamento_nova_carajas', 'Loteamento Nova Carajás'),
        ('loteamento_paraiso_maranhaozinho', 'Loteamento Paraíso Maranhãozinho'),
        ('maranhao', 'Maranhão'),
        ('martini', 'Martini'),
        ('minerios', 'Minérios'),
        ('minas_gerais', 'Minas Gerais'),
        ('mirante_da_serra', 'Mirante da Serra'),
        ('montes_claros', 'Montes Claros'),
        ('morar_dias_melhores', 'Morar Dias Melhores'),
        ('morada_nova', 'Morada Nova'),
        ('nova_capital', 'Nova Capital'),
        ('nova_carajas', 'Nova Carajás'),
        ('nova_esperanca', 'Nova Esperança'),
        ('nova_parauapebas', 'Nova Parauapebas'),
        ('nova_vida', 'Nova Vida'),
        ('nova_vitoria', 'Nova Vitória'),
        ('novo_brasil', 'Novo Brasil'),
        ('novo_horizonte', 'Novo Horizonte'),
        ('novo_tempo', 'Novo Tempo'),
        ('novo_viver', 'Novo Viver'),
        ('nucleo_residencial_servicos_carajas', 'Núcleo Residencial e de Serviços Carajás'),
        ('nucleo_urbano_carajas', 'Núcleo Urbano de Carajás'),
        ('palmares_1', 'Palmares 1'),
        ('palmares_2', 'Palmares 2'),
        ('paraiso', 'Paraíso'),
        ('parque_das_nacoes', 'Parque das Nações'),
        ('parque_dos_carajas', 'Parque dos Carajás'),
        ('parque_sao_luiz', 'Parque São Luiz'),
        ('parque_verde', 'Parque Verde'),
        ('paulo_fonteles', 'Paulo Fonteles'),
        ('polo_industrial_moveleiro', 'Polo Industrial Moveleiro'),
        ('polo_moveleiro', 'Polo Moveleiro'),
        ('porto_seguro', 'Porto Seguro'),
        ('primavera', 'Primavera'),
        ('raio_do_sol', 'Raio do Sol'),
        ('residencial_bambui', 'Residencial Bambuí'),
        ('residencial_belavista', 'Residencial Belavista'),
        ('rio_verde', 'Rio Verde'),
        ('santa_cruz', 'Santa Cruz'),
        ('santa_luzia', 'Santa Luzia'),
        ('sansao', 'Sansão'),
        ('sao_jose', 'São José'),
        ('sao_lucas', 'São Lucas'),
        ('sao_lucas_1', 'São Lucas 1'),
        ('sao_lucas_2', 'São Lucas 2'),
        ('serra_azul', 'Serra Azul'),
        ('talisma', 'Talismã'),
        ('tropical', 'Tropical'),
        ('uniao', 'União'),
        ('vale_do_sol', 'Vale do Sol'),
        ('vale_dos_carajas', 'Vale dos Carajás'),
        ('vale_dos_sonhos', 'Vale dos Sonhos'),
        ('vila_onalicio_barros', 'Vila Onalício Barros'),
        ('vila_nova', 'Vila Nova'),
        ('vila_rica', 'Vila Rica'),
        ('vila_rio_branco', 'Vila Rio Branco'),
        ('vila_sansao', 'Vila Sansão'),
        ('vila_sao_jose', 'Vila São José'),
        ('zona_rural', 'Zona Rural'),
        ('outros', 'Outros'),
        ('outra_cidade', 'Outra cidade'),
    ]

    nome_completo = models.CharField('Nome Completo', max_length=100)
    nome_social = models.CharField('Nome Social', max_length=100, blank=True, null=True)
    data_nascimento = models.DateField('Data de Nascimento')
    CPF = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato XXX.XXX.XXX-XX'
            )
        ]
    )
    telefone = models.CharField(
        'Telefone',
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (XX) XXXXX-XXXX'
            )
        ]
    )
    email = models.EmailField('E-mail', blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES)
    cidade = models.CharField('Cidade', max_length=100)
    bairro = models.CharField('Bairro', max_length=50, choices=BAIRROS_CHOICES, default='outros')
    foto = models.ImageField('Foto', upload_to='visitantes/', blank=True, null=True)

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['nome_completo']

    def __str__(self):
        if self.nome_social:
            return f"{self.nome_social} ({self.nome_completo})"
        return self.nome_completo

    def clean(self):
        if not self.nome_completo:
            raise ValidationError({'nome_completo': 'O nome completo é obrigatório.'})
        if not self.CPF:
            raise ValidationError({'CPF': 'O CPF é obrigatório.'})
        if not self.telefone:
            raise ValidationError({'telefone': 'O telefone é obrigatório.'})
        if not self.cidade:
            raise ValidationError({'cidade': 'A cidade é obrigatória.'})
        if not self.bairro:
            raise ValidationError({'bairro': 'O bairro é obrigatório.'})

class Visita(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ]

    OBJETIVO_CHOICES = [
        ('reuniao', 'Reunião'),
        ('entrega', 'Entrega'),
        ('manutencao', 'Manutenção'),
        ('evento', 'Evento'),
        ('outros', 'Outros')
    ]

    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('plenario', 'Plenário'),
        ('primeiro_piso', '1° Piso'),
        ('segundo_piso', '2° Piso')
    ]

    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.PROTECT,
        verbose_name='Visitante'
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        verbose_name='Setor',
        related_name='visitas'
    )
    localizacao = models.CharField(
        'Localização',
        max_length=20,
        choices=LOCALIZACAO_CHOICES,
        default='terreo'
    )
    objetivo = models.CharField(
        'Objetivo',
        max_length=20,
        choices=OBJETIVO_CHOICES,
        default='outros'
    )
    observacoes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    data_entrada = models.DateTimeField(
        'Data/Hora de Entrada',
        default=timezone.now
    )
    data_saida = models.DateTimeField(
        'Data/Hora de Saída',
        blank=True,
        null=True
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='em_andamento'
    )

    def clean(self):
        if self.status == 'finalizada' and not self.data_saida:
            raise ValidationError({
                'data_saida': 'Data/Hora de Saída é obrigatória para visitas finalizadas'
            })

    def __str__(self):
        return f'{self.visitante} - {self.setor}'
        
    def duracao(self):
        """Calcula a duração da visita em formato legível."""
        if not self.data_saida:
            return None
            
        # Calcula a diferença entre data de saída e entrada
        delta = self.data_saida - self.data_entrada
        
        # Calcula horas, minutos e segundos
        total_segundos = int(delta.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        
        # Formata a duração
        if horas > 0:
            return f"{horas}h {minutos}min"
        else:
            return f"{minutos}min"

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-data_entrada']
