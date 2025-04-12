from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Configuração do Admin
admin.site.site_header = 'URUTAU - Administração'
admin.site.site_title = 'URUTAU'
admin.site.index_title = 'Administração do Sistema'
admin.site.logout = auth_views.LogoutView.as_view(next_page='autenticacao:login_sistema')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('auth/', include('apps.autenticacao.urls', namespace='autenticacao')),
    
    # Apps principais
    path('recepcao/', include('apps.recepcao.urls', namespace='recepcao')),
    path('veiculos/', include('apps.veiculos.urls', namespace='veiculos')),
    
    # Home do sistema
    path('', include('apps.main.urls', namespace='main')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Para servir arquivos de mídia

# Configuração para servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)