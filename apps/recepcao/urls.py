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
    path('buscar-setores/', views.buscar_setores, name='buscar_setores'),
    path('setores/buscar/', views.buscar_setores, name='buscar_setores'),
    path('setores/<int:pk>/excluir/', views.excluir_setor, name='excluir_setor'),
    
    # URLs para reconhecimento facial
    path('visitantes/<int:visitante_id>/upload-foto/', views.upload_foto_visitante, name='upload_foto_visitante'),
    path('visitantes/<int:visitante_id>/registrar-face/', views_face.registrar_face, name='registrar_face'),
    path('video-feed/', views_face.video_feed, name='video_feed'),
    path('api/verificar-face/', views_face.verificar_face_api, name='verificar_face_api'),
    path('teste-camera/', views.teste_camera, name='teste_camera'),
    path('api/cadastro-rapido/', views_face.cadastro_rapido_api, name='cadastro_rapido_api'),
    path('api/registrar-visita/', views_face.registrar_visita_api, name='registrar_visita_api'),
    path('api/parar-reconhecimento/', views_face.parar_reconhecimento_api, name='parar_reconhecimento_api'),
    
    # URLs do totem
    path('totem/', views.totem_visitas, name='totem_visitas'),
    path('totem/home/', views.totem_home, name='totem_home'),
    path('totem/finalizar-visita/', views.totem_finalizar_visita, name='totem_finalizar_visita'),
    
    path('visitantes/<int:pk>/excluir/', views.excluir_visitante, name='excluir_visitante'),
    
    # URLs para AJAX do admin
    path('get_assessores/', views.get_assessores_por_tipo, name='get_assessores_por_tipo'),
    path('get_assessor_info/', views.get_assessor_info, name='get_assessor_info'),
    path('gabinetes/', views.home_gabinetes, name='home_gabinetes'),
    path('gabinetes/<int:gabinete_id>/', views.detalhes_gabinete, name='detalhes_gabinete'),
    path('gabinetes/<int:gabinete_id>/editar/', views.editar_gabinete, name='editar_gabinete'),
    path('departamentos/', views.home_departamentos, name='home_departamentos'),
    path('departamentos/<int:departamento_id>/', views.detalhes_departamento, name='detalhes_departamento'),
]