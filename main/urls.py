from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from veiculos import views as veiculos_views  # Importa as views do app veiculos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.register, name='registro'),
    path('registrar_visita/', views.registrar_visita, name='registrar_visita'),
    path('fim_visita/<int:visita_id>/', views.fim_visita, name='fim_visita'),
    path('entrada_veiculo/', veiculos_views.registrar_entrada, name='entrada_veiculo'),  # Adiciona a view de entrada de veiculo
    path('saida_veiculo/<int:veiculo_id>/', veiculos_views.registrar_saida, name='saida_veiculo'),  # Adiciona a view de saida de veiculo
    path('', views.home, name='home'),  # Adiciona a view home
]