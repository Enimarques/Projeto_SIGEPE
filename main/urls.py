from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('recepcao/', views.recepcao, name='recepcao'),
    path('cadastrar-visitante/', views.cadastrar_visitante, name='cadastrar_visitante'),
    path('lista-visitantes/', views.lista_visitantes, name='lista_visitantes'),
    path('visitas/cadastrar/', views.cadastrar_visita, name='cadastrar_visita'),
    path('visitas/', views.lista_visitas, name='lista_visitas'),
    path('visitas/<int:visita_id>/saida/', views.registrar_saida, name='registrar_saida'),
    
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:login'), name='logout'),
]