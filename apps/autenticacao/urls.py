from django.urls import path, re_path
from .views import login_sistema, logout_sistema
from . import views_usuario
from .user_views.user_views import perfil_usuario

app_name = 'autenticacao'

urlpatterns = [
    # URLs principais do sistema
    path('login/', login_sistema, name='login_sistema'),
    path('logout/', logout_sistema, name='logout_sistema'),
    
    # URLs de gerenciamento de usuários
    path('usuarios/', views_usuario.lista_usuarios, name='lista_usuarios'),
    path('usuarios/novo/', views_usuario.cadastro_usuario, name='criar_usuario'),
    path('usuarios/<int:pk>/editar/', views_usuario.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/excluir/', views_usuario.excluir_usuario, name='excluir_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    
    # URLs de compatibilidade com o Django Admin
    re_path(r'^login/$', login_sistema),  # URL sem nome para compatibilidade com o admin

    # URLs de redirecionamento para manter compatibilidade
    path('assessor/login/', login_sistema, name='login_assessor'),  # Redireciona para login unificado
    path('assessor/logout/', logout_sistema, name='logout_assessor'),  # Redireciona para logout unificado
]
