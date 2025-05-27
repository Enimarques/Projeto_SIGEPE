from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/cards/', views.api_cards, name='api_cards'),
    path('api/graficos/', views.api_graficos, name='api_graficos'),
    path('api/tabela/', views.api_tabela, name='api_tabela'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
] 