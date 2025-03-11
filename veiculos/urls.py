from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.lista_veiculos, name='lista_veiculos'),
    path('entrada/', views.entrada_veiculo, name='entrada_veiculo'),
    path('saida/', views.saida_veiculo, name='saida_veiculo'),
    path('detalhes/<str:placa>/', views.detalhes_veiculo, name='detalhes_veiculo'),
]