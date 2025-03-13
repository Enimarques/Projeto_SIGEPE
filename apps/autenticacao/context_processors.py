from django.urls import reverse

def admin_login_url(request):
    """
    Adiciona a URL de login personalizada ao contexto do admin
    """
    return {
        'admin_login_url': reverse('autenticacao:login_sistema')
    }
