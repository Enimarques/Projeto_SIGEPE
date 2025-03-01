from django.urls import path, include
from django.contrib.auth import views as auth_views #importando as views do django para autenticação
from . import views

urlpatterns = [
    #path('home/', views.home, name='home'), #rota para home
    path('login/', auth_views.LoginView.as_view(), name='login'), #rota para login, usando a padrao do django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), #rota para logout, usando a padrao do django
    path('registro/', views.register, name='registro'), #rota para registro de usuario  
    path('registrar_visita/', views.registrar_visita, name='registrar_visita/'), #rota para registro de visitas
    path('fim_visita/', views.fim_visita, name='fim_visita'), #rota para registrar saida de visitas
    path('Veiculos/', include('veiculos.urls')), #rota para listar veiculos
    ]