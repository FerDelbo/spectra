from django.urls import path
from . import views

urlpatterns = [
    path('minhas-turmas/', views.minhas_turmas, name='minhas_turmas'),
    # Tela de Registro de FO
    path('registrar-fo/<int:aluno_id>/', views.registrar_fo, name='registrar_fo'),
    # APIs para filtro em cascata
    path('get-series/', views.get_series, name='get_series'),
    path('get-turmas/', views.get_turmas, name='get_turmas'),
    path('get-titulos/', views.get_titulos, name='get_titulos'),
]