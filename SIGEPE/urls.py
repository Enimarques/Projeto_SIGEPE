from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Configuração do Admin
admin.site.site_header = 'URUTAU - Administração'
admin.site.site_title = 'URUTAU Admin'
admin.site.index_title = 'Administração do Sistema'

# Configuração do logout do admin para usar nossa view personalizada
admin.site.logout = auth_views.LogoutView.as_view(next_page='autenticacao:login_sistema')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('veiculos/', include('apps.veiculos.urls', namespace='veiculos')),
    path('autenticacao/', include('apps.autenticacao.urls', namespace='autenticacao')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)