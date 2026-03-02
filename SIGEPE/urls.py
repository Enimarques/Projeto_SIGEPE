from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve

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
    path('recepcao/', include('apps.recepcao.urls')),
    path('gabinetes/', include('apps.gabinetes.urls', namespace='gabinetes')),
    path('veiculos/', include('apps.veiculos.urls', namespace='veiculos')),
    path('relatorios/', include('apps.relatorios.urls')),
    
    # Home do sistema
    path('', include('apps.main.urls')),
]

# Configuração para servir arquivos estáticos e de mídia
# Em desenvolvimento, serve STATIC e MEDIA via Django
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Em produção, WhiteNoise serve STATIC, mas MEDIA precisa de servidor web (ex.: Nginx)
    # Fallback temporário para servir MEDIA via Django até configuração do Nginx
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]