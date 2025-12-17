from django.urls import path
from . import views
urlpatterns = [
    path('', views.minhas_turmas, name='minhas_turmas'),
    path('registrar-fo/<int:aluno_id>/', views.registrar_fo, name='registrar_fo'),
    ]