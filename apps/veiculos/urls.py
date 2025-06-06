from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    # Home e Listagem
    path('', views.home_veiculos, name='home_veiculos'),
    path('lista-veiculos/', views.lista_veiculos, name='lista_veiculos'),
    path('lista-veiculos/ajax/', views.lista_veiculos_ajax, name='lista_veiculos_ajax'),
    
    # Registro de Entrada e Saída
    path('registro-entrada/', views.registro_entrada, name='registro_entrada'),
    path('registro-saida/', views.registro_saida, name='registro_saida'),
    
    # Histórico
    path('historico/', views.historico_veiculos, name='historico'),
    path('historico/ajax/', views.historico_veiculos_ajax, name='historico_veiculos_ajax'),
    path('historico/exportar-pdf/', views.exportar_historico_pdf, name='exportar_historico_pdf'),
    path('historico/exportar-excel/', views.exportar_historico_excel, name='exportar_historico_excel'),
    
    # Exportação
    path('veiculos/exportar-pdf/', views.exportar_veiculos_pdf, name='exportar_veiculos_pdf'),
    path('veiculos/exportar-excel/', views.exportar_veiculos_excel, name='exportar_veiculos_excel'),
    
    # Bloqueio
    path('bloquear/<int:veiculo_id>/', views.bloquear_veiculo, name='bloquear_veiculo'),
    path('desbloquear/<int:veiculo_id>/', views.desbloquear_veiculo, name='desbloquear_veiculo'),
    
    path('veiculo-info/', views.veiculo_info_json, name='veiculo_info_json'),
    path('veiculo-info-por-placa/', views.veiculo_info_por_placa_json, name='veiculo_info_por_placa_json'),
]