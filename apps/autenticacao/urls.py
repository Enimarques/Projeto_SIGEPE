from django.urls import path, re_path
from . import views

app_name = 'autenticacao'

urlpatterns = [
    # URLs principais do sistema
    path('login/', views.login_sistema, name='login_sistema'),
    path('logout/', views.logout_sistema, name='logout_sistema'),
    
    # URLs de compatibilidade com o Django Admin
    re_path(r'^login/$', views.login_sistema),  # URL sem nome para compatibilidade com o admin
]
