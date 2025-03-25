from django.urls import path
from . import views

app_name = 'gabinetes'

urlpatterns = [
    path('', views.home_gabinetes, name='home_gabinetes'),
    path('detalhes/<int:pk>/', views.detalhes_gabinete, name='detalhes_gabinete'),
    path('finalizar-visita/<int:visita_id>/', views.finalizar_visita, name='finalizar_visita'),
]
