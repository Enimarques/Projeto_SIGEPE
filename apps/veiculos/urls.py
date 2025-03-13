from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    # Home e Listagem
    path('', views.home_veiculos, name='home_veiculos'),
    path('lista-veiculos/', views.lista_veiculos, name='lista_veiculos'),
    
    # Registro de Entrada e Saída
    path('registro-entrada/', views.registro_entrada, name='registro_entrada'),
    path('registro-saida/', views.registro_saida, name='registro_saida'),
    path('registro-saida/<int:veiculo_id>/', views.registrar_saida, name='registrar_saida'),
]