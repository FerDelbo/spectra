from django.urls import path
from processo import views as processo_views
from . import views

urlpatterns = [
    path('', views.meus_fos, name='meus_fos'),
    path('historico/<int:aluno_id>/', views.historico_aluno, name='historico_aluno'),
    path('observacao/<int:fo_id>/', views.observacao_detalhes, name='observacao_detalhes'),
    path('media/anexo/<path:path>', processo_views.baixar_anexo_seguro, name='baixar_anexo_seguro'),
]