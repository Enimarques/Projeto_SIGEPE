from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_sistema, name='home_sistema'),
    path('api/metricas/', views.metricas_sistema, name='metricas_sistema'),
]
