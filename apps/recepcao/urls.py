from django.urls import path
from . import views, views_face

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
    path('visitas/historico/', views.historico_visitas, name='historico_visitas'),
    path('visitas/<int:visita_id>/finalizar/', views.finalizar_visita, name='finalizar_visita'),
    path('visitas/<int:pk>/excluir/', views.excluir_visita, name='excluir_visita'),
    path('visitas/<int:visita_id>/etiqueta/', views.gerar_etiqueta, name='gerar_etiqueta'),
    path('visitantes/buscar/', views.buscar_visitante, name='buscar_visitante'),
    path('setores/buscar/', views.buscar_setores, name='buscar_setores'),
    # URLs para reconhecimento facial
    path('visitantes/<int:visitante_id>/registrar-face/', views.registrar_face, name='registrar_face'),
    path('visitantes/verificar-face/', views.verificar_face, name='verificar_face'),
    path('visitantes/verificar-face-frame/', views.verificar_face_frame, name='verificar_face_frame'),
    path('totem/', views.totem_visitas, name='totem_visitas'),
    path('visitantes/<int:pk>/excluir/', views.excluir_visitante, name='excluir_visitante'),
]