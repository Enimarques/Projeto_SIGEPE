from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from datetime import datetime, time
import base64
import numpy as np
import logging
import os
from .utils.image_utils import process_image
from .utils.facial_recognition_utils import get_face_embedding
from django.utils.text import slugify

def get_visitor_upload_path(instance, filename):
    """
    Cria um caminho de upload usando nome, sobrenome e ano de nascimento.
    Ex: media/fotos_visitantes/ariel-silva-1988/foto.jpg
    """
    parts = instance.nome_completo.split()
    nome = parts[0]
    sobrenome = parts[-1] if len(parts) > 1 else ''
    ano = instance.data_nascimento.year

    base_folder_name = f"{nome} {sobrenome} {ano}"
    safe_folder_name = slugify(base_folder_name)
    
    return f'fotos_visitantes/{safe_folder_name}/{filename}'

class Setor(models.Model):
    TIPO_CHOICES = [
        ('gabinete', 'Gabinete'),
        ('departamento', 'Departamento')
    ]

    LOCALIZACAO_CHOICES = [
        ('terreo', 'Térreo'),
        ('plenario', 'Plenário'),
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

    # Campos comuns
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    localizacao = models.CharField('Localização', max_length=20, choices=LOCALIZACAO_CHOICES)
    foto = models.ImageField('Foto', upload_to='setores/', blank=True, null=True, help_text='Foto do setor/responsável')
    horario_abertura = models.TimeField('Horário de Abertura', blank=True, null=True)
    horario_fechamento = models.TimeField('Horário de Fechamento', blank=True, null=True)
    
    # Campos específicos para Gabinete
    nome_vereador = models.CharField(max_length=100, verbose_name="Nome do Vereador/Responsável")
    email_vereador = models.EmailField('E-mail do Vereador', max_length=255, blank=True, null=True)
    
    # Campos específicos para Departamento
    nome_local = models.CharField('Nome do Local', max_length=100, blank=True, null=True)
    
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
        ordering = ['tipo', 'localizacao']

    def __str__(self):
        if self.tipo == 'gabinete':
            return self.nome_vereador or 'Gabinete sem nome'
        else:
            return self.nome_local or 'Departamento sem nome'

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
        # Validar campos obrigatórios baseado no tipo
        if self.tipo == 'gabinete':
            if not self.nome_vereador:
                raise ValidationError('O nome do vereador é obrigatório para gabinetes.')
            if not self.email_vereador:
                raise ValidationError('O e-mail do vereador é obrigatório para gabinetes.')
        else:
            if not self.nome_local:
                raise ValidationError('O nome do local é obrigatório para departamentos.')

        # Validar se o horário do responsável está dentro do horário do setor
        if self.horario_entrada and self.horario_saida and self.horario_abertura and self.horario_fechamento:
            if self.horario_entrada < self.horario_abertura or self.horario_saida > self.horario_fechamento:
                raise ValidationError('O horário do responsável deve estar dentro do horário de funcionamento do setor.')
        super().clean()


class Assessor(models.Model):
    """
    Modelo para representar os assessores dos departamentos.
    """
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
        ('chefe_de_gabinete', 'Chefe de Gabinete'),
        ('vereador', 'Vereador'),
        ('outros', 'Outros')
    ]

    nome_responsavel = models.CharField('Nome', max_length=100)
    departamento = models.ForeignKey(
        'Setor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Departamento'
    )
    funcao = models.CharField(
        'Função',
        max_length=20,
        choices=FUNCAO_CHOICES,
        default='assessor_1'
    )
    email = models.EmailField('E-mail', max_length=100, blank=True, null=True)
    horario_entrada = models.TimeField('Horário de Entrada', null=True, blank=True)
    horario_saida = models.TimeField('Horário de Saída', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    usuario = models.OneToOneField(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assessor',
        verbose_name='Usuário'
    )

    class Meta:
        verbose_name = 'Assessor'
        verbose_name_plural = 'Assessores'
        ordering = ['nome_responsavel']

    def __str__(self):
        if self.departamento:
            if self.departamento.tipo == "gabinete":
                departamento_nome = self.departamento.nome_vereador or 'Gabinete'
            else:
                departamento_nome = self.departamento.nome_local or 'Departamento'
            return f'{self.nome_responsavel} - {self.get_funcao_display()} ({departamento_nome})'
        return f'{self.nome_responsavel} - {self.get_funcao_display()} (Sem departamento)'

    def clean(self):
        if self.horario_entrada and self.horario_saida:
            if self.horario_entrada >= self.horario_saida:
                raise ValidationError({
                    'horario_entrada': 'O horário de entrada deve ser anterior ao horário de saída.',
                    'horario_saida': 'O horário de saída deve ser posterior ao horário de entrada.'
                })

            if self.departamento:
                if self.horario_entrada < self.departamento.horario_abertura:
                    raise ValidationError({
                        'horario_entrada': 'O horário de entrada não pode ser anterior ao horário de abertura do departamento.'
                    })
                if self.horario_saida > self.departamento.horario_fechamento:
                    raise ValidationError({
                        'horario_saida': 'O horário de saída não pode ser posterior ao horário de fechamento do departamento.'
                    })

    def get_horario_trabalho(self):
        """Retorna o horário de trabalho formatado."""
        if self.horario_entrada and self.horario_saida:
            return f'{self.horario_entrada.strftime("%H:%M")} - {self.horario_saida.strftime("%H:%M")}'
        return 'Não definido'
    get_horario_trabalho.short_description = 'Horário de Trabalho'

    def get_status_presenca(self):
        """Retorna o status de presença do assessor."""
        if not self.horario_entrada or not self.horario_saida:
            return False

        hora_atual = timezone.localtime().time()
        return self.horario_entrada <= hora_atual <= self.horario_saida
    get_status_presenca.short_description = 'Presente'
    get_status_presenca.boolean = True

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

    # Dados Pessoais
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
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
    
    # Endereço
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES)
    cidade = models.CharField('Cidade', max_length=100)
    bairro = models.CharField('Bairro', max_length=50, choices=BAIRROS_CHOICES, default='outros')
    logradouro = models.CharField('Logradouro', max_length=100, blank=True, null=True)
    numero = models.CharField('Número', max_length=10, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=50, blank=True, null=True)
    CEP = models.CharField(
        'CEP',
        max_length=9,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='CEP deve estar no formato 00000-000'
            )
        ]
    )

    # Fotos em diferentes tamanhos
    foto = models.ImageField('Foto Original', upload_to=get_visitor_upload_path, blank=True, null=True)
    foto_thumbnail = models.ImageField('Foto Thumbnail', upload_to=get_visitor_upload_path, blank=True, null=True)
    foto_medium = models.ImageField('Foto Média', upload_to=get_visitor_upload_path, blank=True, null=True)
    foto_large = models.ImageField('Foto Grande', upload_to=get_visitor_upload_path, blank=True, null=True)
    biometric_vector = models.JSONField(verbose_name="Vetor Biométrico", null=True, blank=True, editable=False)

    # Datas de Controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def save(self, *args, **kwargs):
        # Manter controle da foto antiga
        old_instance = None
        if self.pk:
            try:
                old_instance = Visitante.objects.get(pk=self.pk)
            except Visitante.DoesNotExist:
                pass  # O objeto é novo, não há instância antiga

        # Se a foto foi alterada, a nova foto estará em self.foto
        # e a antiga em old_instance.foto
        new_photo_uploaded = False
        if old_instance and self.foto != old_instance.foto:
            new_photo_uploaded = True
            # Deletar os arquivos de foto antigos
            if old_instance.foto:
                old_instance.foto.delete(save=False)
            if old_instance.foto_thumbnail:
                old_instance.foto_thumbnail.delete(save=False)
            if old_instance.foto_medium:
                old_instance.foto_medium.delete(save=False)
            if old_instance.foto_large:
                old_instance.foto_large.delete(save=False)
            
            # Como a foto mudou, o vetor biométrico antigo não é mais válido
            self.biometric_vector = None

        # Processa a nova foto (seja no cadastro ou na edição)
        if self.foto and (new_photo_uploaded or not self.pk):
            try:
                # Gerar vetor biométrico
                self.biometric_vector = get_face_embedding(self.foto)
                
                # Processar e salvar as diferentes versões da imagem
                processed_images = process_image(self.foto)
                self.foto_thumbnail = processed_images.get('thumbnail')
                self.foto_medium = processed_images.get('medium')
                self.foto_large = processed_images.get('large')

            except (ValueError, Exception) as e:
                # Em caso de erro (ex: rosto não detectado), não bloqueie o salvamento
                # Apenas registre o erro. A validação principal deve ser no formulário.
                logging.error(f"Erro ao processar imagem ou vetor para {self.nome_completo}: {e}")
                # Limpa os campos de imagem para evitar inconsistência
                self.foto_thumbnail = None
                self.foto_medium = None
                self.foto_large = None
                self.biometric_vector = None

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Deletar todos os arquivos de foto do armazenamento antes de deletar o objeto
        if self.foto:
            self.foto.delete(save=False)
        if self.foto_thumbnail:
            self.foto_thumbnail.delete(save=False)
        if self.foto_medium:
            self.foto_medium.delete(save=False)
        if self.foto_large:
            self.foto_large.delete(save=False)
        
        super().delete(*args, **kwargs)

    def get_foto_url(self, size='medium'):
        """
        Retorna a URL da foto no tamanho especificado.
        Usa cache para evitar processamento desnecessário.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        from django.core.cache import cache
        
        # Tenta pegar do cache primeiro
        cache_key = f'visitante_foto_{self.id}_{size}'
        cached_url = cache.get(cache_key)
        if cached_url:
            logger.debug(f"Cache hit para visitante {self.id}, tamanho {size}: {cached_url}")
            return cached_url
            
        # Se não está no cache, pega a URL apropriada
        foto_field = getattr(self, f'foto_{size}', None) or self.foto
        
        if foto_field and hasattr(foto_field, 'url'):
            url = foto_field.url
            logger.debug(f"URL gerada para visitante {self.id}, tamanho {size}: {url}")
            # Cache por 1 hora
            cache.set(cache_key, url, 3600)
            return url
        
        logger.warning(f"Nenhuma foto encontrada para visitante {self.id}, tamanho {size}")
        return None

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = 'Visitantes'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    def clean(self):
        super().clean()
        if self.bairro and not self.cidade:
            raise ValidationError({'cidade': 'A cidade é obrigatória se o bairro for informado.'})
        if self.CEP and len(re.sub(r'[^0-9]', '', self.CEP)) != 8:
            raise ValidationError({'CEP': 'O CEP deve conter 8 dígitos.'})
        if self.bairro and not self.logradouro:
            raise ValidationError({'logradouro': 'O logradouro é obrigatório.'})

class Visita(models.Model):
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ]

    OBJETIVO_CHOICES = [
        ('reuniao', 'Reunião'),
        ('manutencao', 'Manutenção'),
        ('evento', 'Evento'),
        ('entrega_documentos', 'Entrega de Documentos'),
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
        verbose_name='Setor'
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
