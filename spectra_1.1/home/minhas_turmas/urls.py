from django.urls import path
from . import views

urlpatterns = [
    # Tela principal com os Cards
    path('minhas-turmas/', views.minhas_turmas, name='minhas_turmas'),

    # Tela interna da Turma (Lista de Alunos) - PRECISA do ID
    path('turma/<int:turma_id>/', views.lista_alunos, name='lista_alunos'),

    # Tela de Registro de FO
    path('registrar-fo/<int:aluno_id>/', views.registrar_fo, name='registrar_fo'),
]