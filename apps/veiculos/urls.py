from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    # Home e Listagem
    path('', views.home_veiculos, name='home_veiculos'),
    path('lista-veiculos/', views.ListaVeiculosView.as_view(), name='lista_veiculos'),
    
    # Registro de Entrada e Saída
    path('registro-entrada/', views.registro_entrada, name='registro_entrada'),
    path('registro-saida/', views.registro_saida, name='registro_saida'),
    
    # Histórico
    path('historico/', views.HistoricoVeiculosView.as_view(), name='historico'),
    path('historico/veiculo/<int:veiculo_id>/', views.historico_veiculo, name='historico_veiculo'),
    path('historico/exportar-pdf/', views.exportar_historico_pdf, name='exportar_historico_pdf'),
    path('historico/exportar-excel/', views.exportar_historico_excel, name='exportar_historico_excel'),
    
    # Exportação
    path('veiculos/exportar-pdf/', views.exportar_veiculos_pdf, name='exportar_veiculos_pdf'),
    path('veiculos/exportar-excel/', views.exportar_veiculos_excel, name='exportar_veiculos_excel'),
    
    # Bloqueio
    path('bloquear/<int:veiculo_id>/', views.bloquear_veiculo, name='bloquear_veiculo'),
    path('desbloquear/<int:veiculo_id>/', views.desbloquear_veiculo, name='desbloquear_veiculo'),
]