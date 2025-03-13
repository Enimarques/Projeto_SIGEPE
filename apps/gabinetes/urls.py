from django.urls import path
from . import views

app_name = 'gabinetes'

urlpatterns = [
    path('', views.home_gabinetes, name='home_gabinetes'),
]
