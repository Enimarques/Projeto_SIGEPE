from django.urls import path, re_path
from . import views, views_usuario, views_assessor

app_name = 'autenticacao'

urlpatterns = [
    # URLs principais do sistema
    path('login/', views.login_sistema, name='login_sistema'),
    path('logout/', views.logout_sistema, name='logout_sistema'),
    
    # URLs de gerenciamento de usuários
    path('usuarios/', views_usuario.lista_usuarios, name='lista_usuarios'),
    path('usuarios/novo/', views_usuario.cadastro_usuario, name='criar_usuario'),
    path('usuarios/<int:pk>/editar/', views_usuario.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/excluir/', views_usuario.excluir_usuario, name='excluir_usuario'),
    
    # URLs de compatibilidade com o Django Admin
    re_path(r'^login/$', views.login_sistema),  # URL sem nome para compatibilidade com o admin

    # URL para login de assessores
    path('assessor/login/', views_assessor.login_assessor, name='login_assessor'),
    path('assessor/logout/', views_assessor.logout_assessor, name='logout_assessor'),
    path('assessor/set-password/<str:token>/', views_assessor.set_password_assessor, name='set_password_assessor'),
]
