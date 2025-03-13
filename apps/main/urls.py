from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Recepção
    path('', views.home_sistema, name='home_sistema'),
    path('recepcao/status-visita/', views.status_visita, name='status_visita'),
    
    # Visitantes
    path('visitantes/cadastro/', views.cadastro_visitantes, name='cadastro_visitantes'),
    path('visitantes/lista/', views.lista_visitantes, name='lista_visitantes'),
    path('visitantes/<int:pk>/', views.detalhes_visitante, name='detalhes_visitante'),
    
    # Visitas
    path('visitantes/visitas/registro/', views.registro_visitas, name='registro_visitas'),
    path('visitantes/visitas/historico/', views.historico_visitas, name='historico_visitas'),
    path('visitantes/visitas/<int:visita_id>/finalizar/', views.finalizar_visita, name='finalizar_visita'),
]