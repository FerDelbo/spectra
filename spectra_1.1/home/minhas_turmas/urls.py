from django.urls import path
from . import views

urlpatterns = [
    path('minhas-turmas/', views.minhas_turmas, name='minhas_turmas'),
    # Tela de Registro de FO
    path('registrar-fo/<int:aluno_id>/', views.registrar_fo, name='registrar_fo'),
]