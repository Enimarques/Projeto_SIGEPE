from django.urls import path, re_path
<<<<<<< HEAD
from . import views, views_usuario, views_assessor
=======
from . import views
from . import views_assessor
>>>>>>> deb59c7c06587b572cc4553da79673b6da1dcbaa

app_name = 'autenticacao'

urlpatterns = [
    # URLs principais do sistema
    path('login/', views.login_sistema, name='login_sistema'),
<<<<<<< HEAD

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
=======
    path('logout/', views.logout_sistema, name='logout_sistema'),
    
    # URLs para assessores
    path('assessor/login/', views_assessor.login_assessor, name='login_assessor'),
    path('assessor/logout/', views_assessor.logout_assessor, name='logout_assessor'),
    path('assessor/set-password/<str:token>/', views_assessor.set_password_assessor, name='set_password_assessor'),
    
    # URLs de compatibilidade com o Django Admin
    re_path(r'^login/$', views.login_sistema),  # URL sem nome para compatibilidade com o admin
>>>>>>> deb59c7c06587b572cc4553da79673b6da1dcbaa
]
