# Generated by Django 5.1.6 on 2025-03-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepcao', '0005_alter_setor_tipo_alter_visita_setor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='bairro',
            field=models.CharField(choices=[('alto_boa_vista', 'Alto da Boa Vista'), ('alto_bonito', 'Alto Bonito'), ('altamira', 'Altamira'), ('amazonia', 'Amazônia'), ('alvora', 'Alvorá'), ('apoena', 'Apoena'), ('amec_ville_jacaranda', 'Amec Ville Jacarandá'), ('beira_rio_1', 'Beira Rio I'), ('beira_rio_2', 'Beira Rio II'), ('belvedere', 'Belvedere'), ('betania', 'Betânia'), ('brasilia', 'Brasília'), ('bom_jesus', 'Bom Jesus'), ('caetanopolis', 'Caetanópolis'), ('casas_populares_1', 'Casas Populares I'), ('casas_populares_2', 'Casas Populares II'), ('california', 'California'), ('cedere_1', 'Cedere I'), ('cedere_2', 'Cedere II'), ('centro', 'Centro'), ('cidade_jardim', 'Cidade Jardim'), ('cidade_nova', 'Cidade Nova'), ('chacara_belo_vale', 'Chacara Belo Vale'), ('chacara_da_lua', 'Chacara da Lua'), ('chacara_das_estrelas', 'Chacara das Estrelas'), ('chacara_do_sol', 'Chacara do Sol'), ('chacara_do_cacau', 'Chacara do Cacau'), ('colonia_paulo_fonteles', 'Colônia Paulo Fonteles'), ('conjunto_hab_morar_dias_melhores', 'Conjunto Hab Morar Dias Melhores'), ('da_paz', 'Da Paz'), ('dos_mineiros', 'Dos Mineiros'), ('distrito_industrial', 'Distrito Industrial'), ('esplanada', 'Esplanada'), ('esperanca', 'Esperança'), ('fap', 'FAP'), ('fazenda_santo_antonio', 'Fazenda Santo Antônio'), ('fazenda_sao_jose', 'Fazenda São José'), ('fazenda_serra_grande', 'Fazenda Serra Grande'), ('guanabara', 'Guanabara'), ('habitar_feliz', 'Habitar Feliz'), ('ipiranga', 'Ipiranga'), ('jardim_america', 'Jardim América'), ('jardim_canada', 'Jardim Canadá'), ('jardim_planalto', 'Jardim Planalto'), ('jardim_ipiranga', 'Jardim Ipiranga'), ('jardim_novo_horizonte', 'Jardim Novo Horizonte'), ('liberdade_1', 'Liberdade I'), ('liberdade_2', 'Liberdade II'), ('linha_verde', 'Linha Verde'), ('loteamento_nova_carajas', 'Loteamento Nova Carajás'), ('loteamento_paraiso_maranhaozinho', 'Loteamento Paraíso Maranhãozinho'), ('maranhao', 'Maranhão'), ('martini', 'Martini'), ('minerios', 'Minérios'), ('minas_gerais', 'Minas Gerais'), ('mirante_da_serra', 'Mirante da Serra'), ('montes_claros', 'Montes Claros'), ('morar_dias_melhores', 'Morar Dias Melhores'), ('morada_nova', 'Morada Nova'), ('nova_capital', 'Nova Capital'), ('nova_carajas', 'Nova Carajás'), ('nova_esperanca', 'Nova Esperança'), ('nova_parauapebas', 'Nova Parauapebas'), ('nova_vida', 'Nova Vida'), ('nova_vitoria', 'Nova Vitória'), ('novo_brasil', 'Novo Brasil'), ('novo_horizonte', 'Novo Horizonte'), ('novo_tempo', 'Novo Tempo'), ('novo_viver', 'Novo Viver'), ('nucleo_residencial_servicos_carajas', 'Núcleo Residencial e de Serviços Carajás'), ('nucleo_urbano_carajas', 'Núcleo Urbano de Carajás'), ('palmares_1', 'Palmares 1'), ('palmares_2', 'Palmares 2'), ('paraiso', 'Paraíso'), ('parque_das_nacoes', 'Parque das Nações'), ('parque_dos_carajas', 'Parque dos Carajás'), ('parque_sao_luiz', 'Parque São Luiz'), ('parque_verde', 'Parque Verde'), ('paulo_fonteles', 'Paulo Fonteles'), ('polo_industrial_moveleiro', 'Polo Industrial Moveleiro'), ('polo_moveleiro', 'Polo Moveleiro'), ('porto_seguro', 'Porto Seguro'), ('primavera', 'Primavera'), ('raio_do_sol', 'Raio do Sol'), ('residencial_bambui', 'Residencial Bambuí'), ('residencial_belavista', 'Residencial Belavista'), ('rio_verde', 'Rio Verde'), ('santa_cruz', 'Santa Cruz'), ('santa_luzia', 'Santa Luzia'), ('sansao', 'Sansão'), ('sao_jose', 'São José'), ('sao_lucas', 'São Lucas'), ('sao_lucas_1', 'São Lucas 1'), ('sao_lucas_2', 'São Lucas 2'), ('serra_azul', 'Serra Azul'), ('talisma', 'Talismã'), ('tropical', 'Tropical'), ('uniao', 'União'), ('vale_do_sol', 'Vale do Sol'), ('vale_dos_carajas', 'Vale dos Carajás'), ('vale_dos_sonhos', 'Vale dos Sonhos'), ('vila_onalicio_barros', 'Vila Onalício Barros'), ('vila_nova', 'Vila Nova'), ('vila_rica', 'Vila Rica'), ('vila_rio_branco', 'Vila Rio Branco'), ('vila_sansao', 'Vila Sansão'), ('vila_sao_jose', 'Vila São José'), ('zona_rural', 'Zona Rural'), ('outros', 'Outros')], default='outros', max_length=50, verbose_name='Bairro'),
        ),
    ]
