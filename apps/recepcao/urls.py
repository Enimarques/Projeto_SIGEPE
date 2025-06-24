from django.urls import path
from . import views

app_name = 'recepcao'

urlpatterns = [
    # Home e Status
    path('', views.home_recepcao, name='home_recepcao'),
    path('visitantes/', views.lista_visitantes, name='lista_visitantes'),
    path('cadastro-visitantes/', views.cadastro_visitantes, name='cadastro_visitantes'),
    path('visitantes/<int:pk>/', views.detalhes_visitante, name='detalhes_visitante'),
    path('visitantes/<int:pk>/editar/', views.editar_visitante, name='editar_visitante'),
    path('visitas/registro/', views.registro_visitas, name='registro_visitas'),
    path('visitas/status/', views.status_visita, name='status_visita'),
    path('visitas/status/ajax/', views.status_visita_ajax, name='status_visita_ajax'),
    path('visitas/historico/', views.historico_visitas, name='historico_visitas'),
    path('visitas/historico/ajax/', views.historico_visitas_ajax, name='historico_visitas_ajax'),
    path('visitas/<int:visita_id>/finalizar/', views.finalizar_visita, name='finalizar_visita'),
    path('visitas/<int:pk>/excluir/', views.excluir_visita, name='excluir_visita'),
    path('visitas/<int:visita_id>/etiqueta/', views.gerar_etiqueta, name='gerar_etiqueta'),
    path('visitantes/buscar/', views.buscar_visitante, name='buscar_visitante'),
    path('buscar-setores/', views.buscar_setores, name='buscar_setores'),
    path('setores/buscar/', views.buscar_setores, name='buscar_setores'),
    path('setores/<int:pk>/excluir/', views.excluir_setor, name='excluir_setor'),
    
    path('visitantes/<int:visitante_id>/upload-foto/', views.upload_foto_visitante, name='upload_foto_visitante'),
    path('upload-foto-webcam/', views.upload_foto_webcam, name='upload_foto_webcam'),
    path('visitantes/<int:pk>/excluir/', views.excluir_visitante, name='excluir_visitante'),
    
    # URLs para AJAX do admin
    path('get_assessores/', views.get_assessores_por_tipo, name='get_assessores_por_tipo'),
    path('get_assessor_info/', views.get_assessor_info, name='get_assessor_info'),
    path('gabinetes/', views.home_gabinetes, name='home_gabinetes'),
    path('gabinetes/<int:gabinete_id>/', views.detalhes_gabinete, name='detalhes_gabinete'),
    path('gabinetes/<int:gabinete_id>/editar/', views.editar_gabinete, name='editar_gabinete'),
    path('gabinetes/<int:gabinete_id>/tabela/', views.visitas_tabela_gabinete, name='tabela_visitas_gabinete'),
    path('departamentos/', views.home_departamentos, name='home_departamentos'),
    path('departamentos/<int:departamento_id>/tabela/', views.visitas_tabela_departamento, name='tabela_visitas_departamento'),
    path('departamentos/<int:departamento_id>/', views.detalhes_departamento, name='detalhes_departamento'),

    # Rota do Totem
    path('totem/', views.totem_identificacao, name='totem_identificacao'),
    path('totem/destino/', views.totem_destino, name='totem_destino'),

    # API Endpoints para o Totem
    path('api/reconhecer-rosto/', views.api_reconhecer_rosto, name='api_reconhecer_rosto'),
    path('api/registrar-visita/', views.api_registrar_visita_totem, name='api_registrar_visita_totem'),
    path('api/get-setores/', views.api_get_setores, name='api_get_setores'),

    # Rota para a tela do comprovante (ticket)
    path('totem/comprovante/<int:visita_id>/', views.totem_comprovante, name='totem_comprovante'),
]