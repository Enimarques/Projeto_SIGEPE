from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('lista/', views.lista_veiculos, name='lista_veiculos'),
    path('registro/entrada/', views.registro_entrada, name='registro_entrada'),
    path('registro/saida/', views.registro_saida, name='registro_saida'),
    path('detalhes/<str:placa>/', views.detalhes_veiculo, name='detalhes_veiculo'),
]