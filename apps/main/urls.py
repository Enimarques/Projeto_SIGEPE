from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_sistema, name='home_sistema'),
]
