from django.urls import path
from . import views

app_name = 'recepcao'

urlpatterns = [
    # Home e Status
    path('', views.home_sistema, name='home_sistema'),
    path('recepcao/', views.home_recepcao, name='home_recepcao'),
    path('status-visita/', views.status_visita, name='status_visita'),
    
    # Visitantes
    path('cadastro-visitantes/', views.cadastro_visitantes, name='cadastro_visitantes'),
    path('lista-visitantes/', views.lista_visitantes, name='lista_visitantes'),
    path('visitantes/<int:pk>/', views.detalhes_visitante, name='detalhes_visitante'),
    
    # Visitas
    path('registro-visitas/', views.registro_visitas, name='registro_visitas'),
    path('historico-visitas/', views.historico_visitas, name='historico_visitas'),
    path('visitas/<int:visita_id>/finalizar/', views.finalizar_visita, name='finalizar_visita'),
]