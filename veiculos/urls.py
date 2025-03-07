from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/estac/', auth_views.LoginView.as_view(template_name='login_estac.html'), name='login_estac'),
    # path('logout/estac/', auth_views.LogoutView.as_view(next_page='login_estac'), name='logout-estac'),
    # path('home/estac/', views.home_estac, name='home_estac),
]