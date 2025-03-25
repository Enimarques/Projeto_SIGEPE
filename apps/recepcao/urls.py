from django.urls import path
from . import views

app_name = 'recepcao'

urlpatterns = [
    # Home e Status
    path('', views.home_recepcao, name='home_recepcao'),
    path('lista-visitantes/', views.lista_visitantes, name='lista_visitantes'),
    path('cadastro-visitantes/', views.cadastro_visitantes, name='cadastro_visitantes'),
    path('detalhes-visitante/<int:pk>/', views.detalhes_visitante, name='detalhes_visitante'),
    path('registro-visitas/', views.registro_visitas, name='registro_visitas'),
    path('buscar-visitante/', views.buscar_visitante, name='buscar_visitante'),
    path('buscar-setores/', views.buscar_setores, name='buscar_setores'),
    path('historico-visitas/', views.historico_visitas, name='historico_visitas'),
    path('status-visita/', views.status_visita, name='status_visita'),
    path('excluir-visita/<int:pk>/', views.excluir_visita, name='excluir_visita'),
    path('excluir-setor/<int:pk>/', views.excluir_setor, name='excluir_setor'),
    path('finalizar-visita/<int:visita_id>/', views.finalizar_visita, name='finalizar_visita'),
    path('editar-visitante/<int:pk>/', views.editar_visitante, name='editar_visitante'),
    path('gerar-etiqueta/<int:visita_id>/', views.gerar_etiqueta, name='gerar_etiqueta'),  # Adicionando URL para gerar etiqueta
    path('alterar-horario-departamento/', views.alterar_horario_departamento, name='alterar_horario_departamento'),  # URL para alterar horário do departamento
]