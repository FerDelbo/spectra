from django.urls import path
from . import views

urlpatterns = [
    path('', views.meus_fos, name='meus_fos'),
    path('historico/<int:aluno_id>/', views.historico_aluno, name='historico_aluno'),
    path('observacao/<int:fo_id>/', views.observacao_detalhes, name='observacao_detalhes'),
]