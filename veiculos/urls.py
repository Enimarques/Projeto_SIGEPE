from django.urls import path
from . import views

urlpatterns = [
    path('entrada_veiculo/', views.registrar_entrada, name='entrada_veiculo'),
    path('saida_veiculo/<int:veiculo_id>/', views.registrar_saida, name='saida_veiculo'),
    path('listar_veiculos/', views.listar_veiculos, name='listar_veiculos'),  # Adiciona a view de listagem de veículos
]